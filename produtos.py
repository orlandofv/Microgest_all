# -*- coding: latin-1 -*-
"""
Created on Fri Mar 02 23:18:43 2012

@author: lims
"""

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QDoubleSpinBox, QFormLayout, QVBoxLayout, QToolBar, QMessageBox, \
    QTextEdit, QAction, QApplication, QComboBox, QPushButton, QFileDialog, QHBoxLayout, QGroupBox, QPlainTextEdit
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QPixmap
import sys

from utilities import codigo as cd, UNIDADE
from pricespinbox import price

import sqlite3 as lite

filename = "dados.tsdb"


class produto(QDialog):
    def __init__(self, parent=None):
        super(produto, self).__init__(parent)

        self.fotofile = ""

        self.accoes()
        self.ui()

        if self.parent() is None:
            self.db = self.connect_db()
        else:
            self.cur = self.parent().cur
            self.conn = self.parent().conn

        # verifica a existencia dos dados na base de dados
        self.existe(self.cod.text())

        # Mostraregisto caso exista
        self.mostrarReg()

        self.enchefamilia()
        self.enchesubfamilia()

    def ui(self):
        html = """<center style= "{color:blue;}" > <h2 > Cadastro de Produtos </h2> </center> """

        titulo = QLabel(html)

        regex = "[-+]?[0-9]*\.?[0-9]*"

        cod = QLabel("Código/Código de Barras")
        nome = QLabel("Breve Descrição")
        familia = QLabel("Família")
        subfamilia = QLabel("Sub Família")
        nome2 = QLabel("Descrição Detalhada")
        custo = QLabel("Custo")
        preco = QLabel("Preço")
        quantidade = QLabel("Quantidade")
        quantidade_m = QLabel("Quantidade Mínima")
        unidade = QLabel("Unidade de Medida")
        obs = QLabel("Observações")

        self.cod = QLineEdit()
        self.nome = QPlainTextEdit()
        self.familia = QComboBox()
        self.subfamilia = QComboBox()
        self.familia.currentTextChanged.connect(self.enchesubfamilia)
        self.subfamilia.currentTextChanged.connect(self.codsubfamilia)
        self.nome2 = QLineEdit()
        self.custo = price()
        self.preco = price()
        self.quantidade = price()
        self.quantidade_m = price()
        self.unidade = QComboBox()
        self.unidade.addItems(UNIDADE)
        self.obs = QTextEdit()
        self.foto = QLabel()
        self.foto.setMinimumSize(200, 200)
        fotogrid = QGroupBox("FOTO do Produto/Serviço")
        self.adicionarfoto= QPushButton(QIcon("./icons/add.ico"), "Seleccionar foto")
        self.adicionarfoto.clicked.connect(self.seleccionarfoto)
        self.removefoto = QPushButton(QIcon("./icons/remove.ico"), "Remover Foto")
        self.removefoto.clicked.connect(self.removerfoto)
        self.fotodialog = QFileDialog(self, "Seleccionar Foto")
        # self.fotodialog.setFilter("*.jpg", "*.png", "*.bmp", "*.*")

        grid = QFormLayout()

        familiaLayout = QHBoxLayout()
        familaGrid1 = QFormLayout()
        familaGrid1.addRow(familia, self.familia)

        familaGrid2 = QFormLayout()
        familaGrid2.addRow(subfamilia, self.subfamilia)

        familiaLayout.addLayout(familaGrid1)
        familiaLayout.addLayout(familaGrid2)

        grid.addRow(cod, self.cod)
        grid.addRow(nome, self.nome)
        # grid.addRow(nome2, self.nome2)
        grid.addRow(familiaLayout)
        grid.addRow(custo, self.custo)
        grid.addRow(preco, self.preco)
        grid.addRow(quantidade, self.quantidade)
        grid.addRow(quantidade_m, self.quantidade_m)
        grid.addRow(unidade, self.unidade)
        grid.addRow(obs, self.obs)

        mainlayout = QVBoxLayout(self)
        # mainlayout.setContentsMargins(0, 0, 0, 0)

        submainlayout = QHBoxLayout()

        buttonslayout = QHBoxLayout()
        buttonslayout.addWidget(self.adicionarfoto)
        buttonslayout.addWidget(self.removefoto)

        fotolayout = QVBoxLayout()
        fotolayout.addWidget(self.foto)
        fotolayout.addLayout(buttonslayout)

        fotogrid.setLayout(fotolayout)

        submainlayout.addLayout(grid)
        submainlayout.addWidget(fotogrid)

        mainlayout.addWidget(titulo)
        mainlayout.addLayout(submainlayout)
        mainlayout.addWidget(self.tool)
        self.setLayout(mainlayout)

        self.setWindowTitle("Cadastro de produtos")

        style = """
            margin: 0;
            padding: 0;
            border-image:url(./images/transferir.jpg) 30 30 stretch;
            background:#303030;
            font-family: Arial, Helvetica, sans-serif;
            font-size: 12px;
            color: #FFFFFF;
        """

        titulo.setStyleSheet(style)

    def accoes(self):
        self.tool = QToolBar()

        gravar = QAction(QIcon("./images/ok.png"), "&Gravar dados", self)
        eliminar = QAction(QIcon("./images/Delete.ico"), "&Eliminar dados", self)

        fechar = QAction(QIcon("./images/filequit.png"), "&Fechar", self)

        self.tool.addAction(gravar)
        self.tool.addAction(eliminar)

        self.tool.addSeparator()
        self.tool.addAction(fechar)

        gravar.triggered.connect(self.addRecord)
        eliminar.triggered.connect(self.limpar)
        fechar.triggered.connect(self.fechar)

    # Enche a Combobox Familia
    def enchefamilia(self):
        sql = "SELECT nome FROM familia"
        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) == 0:
            QMessageBox.information(self, "Cadastre Familia", "Cadastre Familia Primeiro")
            return

        for item in data:
            self.familia.addItems(item)

    def enchesubfamilia(self):

        # clear the combobox
        self.subfamilia.clear()

        # Procura o nome na tabela familia baseando-se no codigo da Familia na tabela subfamilia
        sql = """select subfamilia.nome from familia INNER JOIN subfamilia ON familia.cod=subfamilia.codfamilia
         where familia.nome= "{nome}" """.format(nome=self.familia.currentText())

        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) == 0:
            QMessageBox.information(self, "Cadastre Sub Familia", "Cadastre Sub Familia Primeiro")
            return

        for item in data:
            self.subfamilia.addItems(item)

        # Encontra o código da
        self.getcodfamilia()

    def codsubfamilia(self):
        sql = """select cod from subfamilia where nome= "{nome}" """.format(nome=self.subfamilia.currentText())
        self.cur.execute(sql)
        data = self.cur.fetchall()

        for item in data:
            self.subfamiliacod = item[0]
    
    def getcodfamilia(self):
        sql = """select cod from familia where nome= "{nome}" """.format(nome=self.familia.currentText())

        self.cur.execute(sql)
        data = self.cur.fetchall()
        self.familiacod = "".join(data[0])
        
    def closeEvent(self, evt):
        parent = self.parent()
        try:
            if parent is not None:
                parent.fill_table()
        except:
            return

    def fechar(self):
        self.close()

    def limpar(self):
        for child in (self.findChildren(QLineEdit) or self.findChildren(QTextEdit) or
                          self.findChildren(QPlainTextEdit)):
            if child.objectName() not in ["cod", "cal1", "cal2"]: child.clear()

        self.nome.setPlainText("")
        self.obs.setPlainText("")
        self.cod.setText("FM" + cd("PR" + "ABCDEF1234567890"))
        self.cod.selectAll()
        self.custo.setValue(0.00)
        self.preco.setValue(0.00)
        self.quantidade.setValue(0.00)
        self.quantidade_m.setValue(0.00)

    def validacao(self):

        if self.custo.text() == "": self.custo.setValue(0.00)
        if self.preco.text() == "": self.preco.setValue(0.00)
        if self.quantidade.text() == "": self.quantidade.setValue(0.00)
        if self.quantidade_m.text() == "": self.quantidade_m.setValue(0.00)

        if str(self.nome.toPlainText()) == "":
            QMessageBox.information(self, "Erro", "Nome do produto inválido")
            self.nome.setFocus()
            return False
        elif str(self.familia.currentText()) == "":
            QMessageBox.information(self, "Erro", "Cadastre Famílias de Produtos Primeiro")
            return False
        elif str(self.subfamilia.currentText()) == "":
            QMessageBox.information(self, "Erro", "Cadastre Sub Famílias de Produtos Primeiro")
            return False
        else:
            return True

    def mostrarReg(self):

        sql = """ SELECT produtos.nome , produtos.nome2, familia.nome, subfamilia.nome, produtos.custo, produtos.preco, 
        produtos.quantidade, produtos.quantidade_m, produtos.unidade, produtos.obs, produtos.foto from familia 
        INNER JOIN produtos ON familia.cod=produtos.codfamilia INNER JOIN subfamilia ON 
        produtos.codsubfamilia=subfamilia.cod where produtos.cod="{codigo}" """.format(codigo=str(self.cod.text()))

        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) == 0:
            self.cod.setText("PR" + cd("ABCDEF1234567890"))
            self.cod.setFocus()
            self.cod.selectAll()
        else:
            self.nome.setPlainText(''.join(data[0][0]))
            self.nome2.setText(''.join(data[0][1]))
            self.familia.setCurrentText(''.join(data[0][2]))
            self.subfamilia.setCurrentText(''.join(data[0][3]))
            self.custo.setValue(data[0][4])
            self.preco.setValue(data[0][5])
            self.quantidade.setValue(data[0][6])
            self.quantidade_m.setValue(data[0][7])
            self.unidade.setCurrentText(''.join(data[0][8]))
            self.obs.setPlainText(''.join(data[0][9]))
            self.foto.setPixmap(QPixmap(''.join(data[0][10])))

    def existe(self, codigo):

        sql = """SELECT cod from produtos where cod = "{codigo}" """.format(codigo=str(self.cod.text()))

        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) == 0:
            codigo = self.cod.text()
            self.codigo = codigo
            return False
        else:
            codigo = ''.join(data[0])
            self.codigo = codigo
            return True

    def seleccionarfoto(self):
        self.fotodialog.open()

    def removerfoto(self):
        self.fotofile = ""
        self.foto.setPixmap(QPixmap(""))

    def addRecord(self):

        if self.validacao() is True:
            code = self.cod.text()
            nome = self.nome.toPlainText()
            familia = self.familiacod
            subfamilia = self.subfamiliacod
            nome2 = self.nome2.text()
            custo = float(self.custo.text())
            preco = float(self.preco.text())
            quantidade = float(self.quantidade.text())
            quantidade_m = float(self.quantidade_m.text())
            unidade = self.unidade.currentText()
            obs = self.obs.toPlainText()
            estado = 1
            created = QDate.currentDate().toString()
            modified = QDate.currentDate().toString()
            foto = self.fotofile

            if self.parent() is not None:
                modified_by = self.parent().user
            else:
                modified_by = "User"
            if self.parent() is not None:
                created_by = self.parent().user
            else:
                created_by = "User"
            if self.existe(code) is True:

                sql = """UPDATE produtos set nome="{nome}", nome2="{nome2}", codfamilia="{familia}",
                 codsubfamilia="{subfamilia}", custo={custo}, preco={preco}, quantidade={quantidade},
                quantidade_m={quantidade_m}, unidade="{unidade}", obs="{obs}", estado={estado}, modified="{modified}", 
                modified_by="{modified_by}", created="{created}", created_by="{created_by}", foto="{foto}" where cod="{cod}"
                """.format(cod=code, nome=nome,familia=familia, subfamilia=subfamilia, nome2=nome2, custo=custo,
                           preco=preco, quantidade=quantidade, quantidade_m=quantidade_m, unidade=unidade, obs=obs,
                           estado=estado, modified=modified, modified_by=modified_by,
                           created=created, created_by=created_by, foto=foto)
                try:
                    self.cur.execute(sql)
                    self.conn.commit()
                except lite.Error as e:
                    QMessageBox.critical(self, "Erro", "Os seus Dados não foram gravados. Erro: {erro} ".format(erro=e))
                    return
            else:
                values = """ "{cod}", "{nome}", "{nome2}","{familia}", "{subfamilia}", {custo}, {preco}, 
                {quantidade}, {quantidade_m}, "{unidade}", "{obs}", {estado}, "{created}", "{modified}", 
                "{modified_by}", "{created_by}", "{foto}"
                  """.format(cod=code, nome=nome, nome2=nome2, familia=familia, subfamilia=subfamilia, custo=custo,
                           preco=preco, quantidade=quantidade, quantidade_m=quantidade_m, unidade=unidade, obs=obs,
                           estado=estado, created=created, modified=modified, modified_by=modified_by,
                             created_by=created_by, foto=foto)

                sql = "INSERT INTO produtos (cod, nome, nome2, codfamilia, codsubfamilia, custo, preco, " \
                      "quantidade, quantidade_m, unidade, obs, estado, created, modified, modified_by," \
                      " created_by, foto) values({value})".format(value=values)
                try:
                    self.cur.execute(sql)
                    self.conn.commit()
                except lite.Error as e:
                    QMessageBox.critical(self, "Erro", "Os seus Dados não foram gravados. Erro: {erro} ".format(erro=e))
                    return

            if QMessageBox.question(self, "Pergunta", "Registo Gravado com sucesso!\nDeseja Cadastrar outro Item?",
                                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                self.limpar()
                self.mostrarReg()
            else:
                self.close()

    def connect_db(self):
        # Connect to database and retrieves data
        try:
            self.conn = lite.connect(filename)
            self.cur = self.conn.cursor()

        except lite.Error as e:
            QMessageBox.critical(self, "Erro ao conectar a Base de Dados",
                                 "Os seus Dados não foram gravados. Erro: {erro} ".format(erro=e))
            sys.exit(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    helloPythonWidget = produto()
    helloPythonWidget.show()

    sys.exit(app.exec_())