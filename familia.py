# -*- coding: latin-1 -*-
"""
Created on Fri Mar 02 23:18:43 2012

@author: lims
"""

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QDoubleSpinBox, QFormLayout, QVBoxLayout, QToolBar, QMessageBox, \
    QTextEdit, QAction, QApplication, QCheckBox
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
import sys

from utilities import codigo as cd
from database import DBCOnnection

import sqlite3 as lite

filename = "dados.tsdb"


class Cliente(QDialog):
    def __init__(self, parent=None):
        super(Cliente, self).__init__(parent)

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

    def ui(self):
        html = """<center style= "{color:blue;}" > <h2 > Cadastro de Famílias </h2> </center> """

        titulo = QLabel(html)

        cod = QLabel("Código da Família")
        nome = QLabel("Descrição")
        obs = QLabel("Observações")

        self.cod = QLineEdit()
        self.cod.setEnabled(False)
        self.nome = QLineEdit()
        self.stock = QCheckBox("Familia diminui Stock")
        self.stock.setChecked(True)
        self.obs = QTextEdit()

        grid = QFormLayout()

        grid.addRow(cod, self.cod)
        grid.addRow(nome, self.nome)
        grid.addRow(self.stock)
        grid.addRow(obs, self.obs)

        vLay = QVBoxLayout(self)
        vLay.setContentsMargins(0, 0, 0, 0)

        cLay = QVBoxLayout()
        cLay.setContentsMargins(10, 10, 10, 10)

        cLay.addLayout(grid)

        vLay.addWidget(titulo)
        vLay.addLayout(cLay)
        vLay.addWidget(self.tool)
        self.setLayout(vLay)

        self.setWindowTitle("Cadastro de Famílias")

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

    # ==============================================================================

    def closeEvent(self, evt):
        parent = self.parent()
        if parent is not None:
            parent.fill_table()

    def fechar(self):
        self.close()

    def limpar(self):
        for child in (self.findChildren(QLineEdit) or self.findChildren(QTextEdit)):
            if child.objectName() not in ["cod", "cal1", "cal2"]: child.clear()

        # gera novo codigo para familia
        self.cod.setText("FM" + cd("FM" + "ABCDEF1234567890"))

    def validacao(self):

        if str(self.nome.text()) == "":
            QMessageBox.information(self, "Erro", "Nome do Cliente inválido")
            self.nome.setFocus()
            return False
        else:
            return True

    def mostrarReg(self):

        sql = """SELECT * from familia where cod = "{codigo}" """.format(codigo=str(self.cod.text()))
        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) == 0:
            self.cod.setText("FM" + cd("ABCDEF1234567890"))
        else:
            self.nome.setText(''.join(data[0][1]))
            if data[0][8] == 1:
                self.stock.setChecked(True)
            else:
                self.stock.setChecked(False)

            self.obs.setPlainText(''.join(data[0][2]))

    def existe(self, codigo):

        sql = """SELECT cod from familia where cod = "{codigo}" """.format(codigo=str(self.cod.text()))

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

    def addRecord(self):

        if self.validacao() is True:
            code = self.cod.text()
            nome = self.nome.text()
            obs = self.obs.toPlainText()
            estado = 1
            created = QDate.currentDate().toString()
            modified = QDate.currentDate().toString()

            if self.stock.isChecked() is True:
                stock = 1
            else:
                stock = 0

            if self.parent() is not None:
                modified_by = self.parent().user
            else:
                modified_by = "User"
            if self.parent() is not None:
                created_by = self.parent().user
            else:
                created_by = "User"
            if self.existe(code) is True:

                sql = """UPDATE familia set nome="{nome}", obs="{obs}", modified="{modified}", 
                modified_by="{modified_by}", stock={stock} where cod="{cod}" 
                """.format(cod=code, nome=nome, obs=obs, modified=modified, modified_by=modified_by, stock=stock)
                try:
                    self.cur.execute(sql)
                    self.conn.commit()
                except lite.Error as e:
                    QMessageBox.critical(self, "Erro", "Os seus Dados não foram gravados. Erro: {erro} ".format(erro=e))
                    return
            else:
                values = """ "{cod}", "{nome}", "{obs}", "{estado}", "{created}", "{modified}", "{modified_by}", 
                "{created_by}", {stock}
                 """.format(cod=code, nome=nome, obs=obs, estado=estado, created=created, modified=modified,
                            modified_by=modified_by, created_by=created_by, stock=stock)
                try:
                    sql = "INSERT INTO familia (cod, nome, obs, estado, created, modified, modified_by, " \
                          "created_by, stock) values({value})".format(value=values)
                    self.cur.execute(sql)
                    self.conn.commit()
                except lite.Error as e:
                    QMessageBox.critical(self, "Erro", "Os seus Dados não foram gravados. Erro: {erro} ".format(erro=e))
                    return

            if QMessageBox.question(self, "Pergunta", "Registo Gravado com sucesso!\nDeseja Cadastrar outro Item?",
                                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                self.limpar()
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

    helloPythonWidget = Cliente()
    helloPythonWidget.show()

    sys.exit(app.exec_())