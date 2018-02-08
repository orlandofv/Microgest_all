# -*- coding: latin-1 -*-
"""
Created on Fri Mar 02 23:18:43 2012

@author: lims
"""

import sys
import decimal

from PyQt5.QtWidgets import  QLabel, QLineEdit, QFormLayout, QVBoxLayout, QToolBar, QMessageBox,\
    QTextEdit, QAction, QApplication, QGroupBox, QPushButton, QComboBox, QDateEdit, QCalendarWidget,\
    QHBoxLayout, QWidget, QTableView, QCheckBox, QAbstractItemView, QSplitter, QDialog

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon

from sortmodel import MyTableModel

from utilities import codigo as cd
from pricespinbox import price
from database import DBCOnnection

import sqlite3 as lite

filename = "dados.tsdb"

class Cliente(QDialog):
    def __init__(self, parent=None):
        super(Cliente, self).__init__(parent)

        self.codfornecedor = ""
        self.codproduto = ""
        self.codarmazem = ""
        self.valortaxa = 0.00
        self.current_id = ""

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

        self.enchefornecedor()
        self.encheprodutos()
        self.enchearmazem()
        self.enchetaxas()

    def ui(self):
        html = """<center style= "{color:blue;}" > <h2 > Cadastro de stock </h2> </center> """

        tablelayout = QHBoxLayout()
        controlslayout = QVBoxLayout()
        controlswidget = QWidget()

        splitter = QSplitter()
        splitter.setOrientation(Qt.Horizontal)

        grupocod = QGroupBox("Código do Documento")
        grupofornecedor = QGroupBox("Detalhes do Documento")
        grupodetalhes = QGroupBox("Items do Documento")

        codlayout = QFormLayout()
        fornecedorlayout = QFormLayout()
        detalheslayout = QFormLayout()

        titulo = QLabel(html)

        titulo.setMaximumHeight(30)

        cod = QLabel("Codigo")
        self.cod = QLineEdit()
        self.cod.setEnabled(False)

        codlayout.addRow(cod, self.cod)
        grupocod.setLayout(codlayout)

        fornecedor = QLabel("Seleccione o Fornecedor")
        documento = QLabel("Numero do documento (Ex. Factura1235)")
        datadocumento = QLabel("Data do Documento")
        valor_documento = QLabel("Valor Total do Documento")
        valor_pago = QLabel("Valor Pago")
        self.gravar_fornecedor = QPushButton("Gravar documento")
        self.gravar_fornecedor.clicked.connect(self.gravardoc)
        self.ativar_fornecedor = QPushButton("Ativar documento")
        self.ativar_fornecedor.clicked.connect(self.habilitarfornecedor)
        self.ativar_fornecedor.setEnabled(False)

        self.fornecedor = QComboBox()
        self.fornecedor.currentIndexChanged.connect(self.getcodfornecedor)
        self.numerodocumento = QLineEdit()
        self.datadocumento = QDateEdit()
        self.datadocumento.setDate(QDate.currentDate())
        calendario = QCalendarWidget()
        self.datadocumento.setCalendarWidget(calendario)
        self.valor_documento = price()
        self.valor_pago = price()
        self.gravardetalhe = QPushButton("Adicionar na Lista")
        self.gravardetalhe.clicked.connect(self.gravardetalhes)
        self.apagarItem = QPushButton("Eliminar Linha")
        self.apagarItem.clicked.connect(self.removerow)
        self.apagarItem.setEnabled(False)

        gravarlayout = QHBoxLayout()

        gravarlayout.addWidget(self.gravar_fornecedor)
        gravarlayout.addWidget(self.ativar_fornecedor)

        fornecedorlayout.addRow(fornecedor, self.fornecedor)
        fornecedorlayout.addRow(documento, self.numerodocumento)
        fornecedorlayout.addRow(datadocumento, self.datadocumento)
        fornecedorlayout.addRow(valor_documento, self.valor_documento)
        fornecedorlayout.addRow(valor_pago, self.valor_pago)
        fornecedorlayout.addRow(gravarlayout)
        grupofornecedor.setLayout(fornecedorlayout)

        produto = QLabel("Seleccione o produto")
        quantidade = QLabel("Quantidade")
        custo = QLabel("Custo do Produto")
        armazem = "Seleccione o Armazém"
        preco = QLabel("Preço Actual")
        taxa = QLabel("Seleccione a Taxa")

        self.produto = QComboBox()
        self.produto.currentIndexChanged.connect(self.getcodproduto)
        self.quantidade = price()
        self.custo = price()
        self.armazem = QComboBox()
        self.armazem.currentIndexChanged.connect(self.getcodarmazem)
        self.preco = price()
        self.preco.setEnabled(False)
        self.taxa = QComboBox()
        self.taxa.currentIndexChanged.connect(self.getvalortaxa)
        self.taxabox = QCheckBox("Preços não incluem taxas")
        self.taxabox.setChecked(True)

        taxagrid = QFormLayout()
        taxagrid.addRow(taxa, self.taxa)

        taxalayout = QHBoxLayout()
        taxalayout.addLayout(taxagrid)
        taxalayout.addWidget(self.taxabox)

        self.tabela = QTableView(self)
        self.tabela.clicked.connect(self.clickedSlot)
        self.tabela.setAlternatingRowColors(True)

        # hide grid
        self.tabela.setShowGrid(False)

        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        # set the font

        # hide vertical header
        vh = self.tabela.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties and stretch last column
        hh = self.tabela.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        self.tabela.resizeColumnsToContents()

        # enable sorting
        self.tabela.setSortingEnabled(True)
        
        butoesdetalheleyout = QHBoxLayout()

        butoesdetalheleyout.addWidget(self.gravardetalhe)
        butoesdetalheleyout.addWidget(self.apagarItem)

        detalheslayout.addRow(produto, self.produto)
        detalheslayout.addRow(quantidade, self.quantidade)
        detalheslayout.addRow(custo, self.custo)
        detalheslayout.addRow(armazem, self.armazem)
        detalheslayout.addRow(preco, self.preco)
        detalheslayout.addRow(taxalayout)
        # detalheslayout.addRow(self.tabela)
        detalheslayout.addRow(butoesdetalheleyout)
        grupodetalhes.setLayout(detalheslayout)

        controlslayout.addWidget(grupocod)
        controlslayout.addWidget(grupofornecedor)
        controlslayout.addWidget(grupodetalhes)

        controlswidget.setLayout(controlslayout)

        splitter.addWidget(controlswidget)
        splitter.addWidget(self.tabela)

        mainlayout = QVBoxLayout()

        mainlayout.addWidget(titulo)
        mainlayout.addWidget(splitter)
        mainlayout.addWidget(self.tool)
        self.setLayout(mainlayout)

        self.setWindowTitle("Cadastro de Clientes")

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
        # eliminar = QAction(QIcon("./images/Delete.ico"), "&Eliminar dados", self)

        fechar = QAction(QIcon("./images/filequit.png"), "&Fechar", self)

        self.tool.addAction(gravar)
        # self.tool.addAction(eliminar)

        self.tool.addSeparator()
        self.tool.addAction(fechar)

        gravar.triggered.connect(self.addRecord)
        # eliminar.triggered.connect(self.limpar)
        fechar.triggered.connect(self.fechar)

    # ==============================================================================
    def fill_table(self):

        header = ["cod", "Documento", "Descrição", "Armazém", "Quantidade", "Preço", "Taxa", "SubTotal", "Total"]

        sql = """ select stockdetalhe.cod, codstock, produtos.nome, armazem.nome, stockdetalhe.quantidade, 
        stockdetalhe.valor, stockdetalhe.taxa, stockdetalhe.subtotal, stockdetalhe.total from produtos INNER JOIN
        stockdetalhe ON produtos.cod=stockdetalhe.codproduto INNER JOIN armazem ON armazem.cod=stockdetalhe.codarmazem 
        where codstock="{codstock}" """.format(codstock=self.cod.text())

        self.cur.execute(sql)
        data = self.cur.fetchall()
        self.tabledata = data

        if len(data) == 0:
            self.apagarItem.setEnabled(False)
            return

        try:
            self.tm = MyTableModel(self.tabledata, header, self)
            # set the table model
            self.totalItems = self.tm.rowCount(self)
            self.tabela.setModel(self.tm)
            self.tabela.setColumnHidden(0, True)
            self.tabela.setColumnHidden(1, True)

        except Exception as e:
            return
        # # set row height
        nrows = len(self.tabledata)
        for row in range(nrows):
            self.tabela.setRowHeight(row, 25)

    def clickedSlot(self, index):

        self.row = int(index.row())

        self.col = int(index.column())

        indice= self.tm.index(self.row, 0)
        self.current_id = indice.data()

        self.fill_data()

        self.apagarItem.setEnabled(True)

    def getcodfornecedor(self):
        sql = """select cod from fornecedores where nome= "{nome}" """.format(nome=self.fornecedor.currentText())

        self.cur.execute(sql)
        data = self.cur.fetchall()
        self.codfornecedor = "".join(data[0])

    def getcodproduto(self):
        sql = """select cod, preco from produtos where nome= "{nome}" """.format(nome=self.produto.currentText())

        self.cur.execute(sql)
        data = self.cur.fetchall()

        self.codproduto = "".join(data[0][0])
        self.preco.setValue(decimal.Decimal(data[0][1]))
        self.custo.setValue(decimal.Decimal(data[0][1]))

    def getcodarmazem(self):
        sql = """select cod from armazem where nome= "{nome}" """.format(nome=self.armazem.currentText())

        self.cur.execute(sql)
        data = self.cur.fetchall()
        self.codarmazem = "".join(data[0])

    def getvalortaxa(self):
        sql = """select valor from taxas where nome= "{nome}" """.format(nome=self.taxa.currentText())

        self.cur.execute(sql)
        data = self.cur.fetchall()

        for item in data[0]:
            self.valortaxa = decimal.Decimal(item)

    def habilitarfornecedor(self):
        self.gravar_fornecedor.setEnabled(True)
        self.desabilitarfornecedor()
        self.ativar_fornecedor.setEnabled(False)

    def desabilitarfornecedor(self):

        self.fornecedor.setEnabled(not self.fornecedor.isEnabled())
        self.numerodocumento.setEnabled(not self.numerodocumento.isEnabled())
        self.datadocumento.setEnabled(not self.datadocumento.isEnabled())
        self.valor_pago.setEnabled(not self.valor_pago.isEnabled())
        self.valor_documento.setEnabled(not self.valor_documento.isEnabled())

    def validacao(self):

        if self.numerodocumento.text() == "":
            QMessageBox.information(self, "Erro de Documento", "Entre o número do documento")
            self.numerodocumento.setFocus()
            return False
        elif self.valor_documento.text() == "":
            self.valor_documento.setValue(0.00)
            return True
        elif self.valor_pago.text() == "":
            self.valor_pago.setValue(0.00)
            return True
        else:
            return True

    def gravardoc(self):

        if self.validacao() is True:
            code = self.cod.text()
            fornecedor = self.codfornecedor
            numero = self.numerodocumento.text()
            data = QDate(self.datadocumento.date()).toString()
            valor = decimal.Decimal(self.valor_documento.text())
            pago = decimal.Decimal(self.valor_pago.text())
            created = QDate.currentDate().toString()
            modified = QDate.currentDate().toString()
            if self.parent() is not None:
                modified_by = self.parent().user
            else:
                modified_by = "User"
            if self.parent() is not None:
                created_by = self.parent().user
            else:
                created_by = "User"


            if self.existe(code) is True:

                sql = """UPDATE stock set fornecedor="{fornecedor}", numero="{numero}", data="{data}", valor={valor}, 
                pago={pago}, modified="{modified}", modified_by="{modified_by}" where cod="{cod}"
                """.format(cod=code, fornecedor=fornecedor, numero=numero, data=data, valor=valor, pago=pago,
                           modified=modified, modified_by=modified_by)
            else:

                values = """ "{cod}", "{fornecedor}", "{numero}", "{data}", {valor}, {pago},  
                "{created}", "{modified}", "{modified_by}", "{created_by}" 
                """.format(cod=code, fornecedor=fornecedor, numero=numero, data=data, valor=valor, pago=pago,
                           created=created, modified=modified, modified_by=modified_by, created_by=created_by)

                sql = "INSERT INTO stock (cod, fornecedor, numero, data, valor, pago, created," \
                      " modified, modified_by, created_by) values({value})".format(value=values)

            try:
                self.cur.execute(sql)
                self.conn.commit()
            except lite.Error as e:
                QMessageBox.critical(self, "Erro", "Os seus Dados não foram gravados. Erro: {erro} ".format(erro=e))
                return

            self.ativar_fornecedor.setEnabled(True)
            self.gravar_fornecedor.setEnabled(False)
            self.desabilitarfornecedor()

    def gravardetalhes(self):

        if self.validacaodetalhes() is True:

            codstock = self.cod.text()
            codproduto = self.codproduto
            codarmazem = self.codarmazem
            quantidade = decimal.Decimal(self.quantidade.text())
            valor = decimal.Decimal(self.custo.text())
            taxa = self.valortaxa / 100

            if self.taxabox.isChecked():
                subtotal = quantidade * valor
            else:
                subtotal = (quantidade * valor)/(taxa + 1)

            valortaxa = subtotal * taxa
            total = subtotal + valortaxa

            if self.existeproduto(codproduto, self.cod.text()) is True:

                sql = """UPDATE stockdetalhe set codstock="{codstock}", codproduto="{codproduto}", 
                codarmazem="{codarmazem}", quantidade={quantidade}, valor={valor}, taxa={taxa}, subtotal={subtotal}, 
                total={total} where codstock="{codstock}" and codproduto="{codproduto}" 
                """.format(codstock=codstock, codproduto=codproduto, codarmazem=codarmazem, quantidade=quantidade,
                           valor=valor, taxa=taxa, subtotal=subtotal, total=total)

            else:

                values = """ "{codstock}", "{codproduto}", "{codarmazem}", {quantidade}, {valor}, {taxa}, {subtotal}, 
                {total} """.format(codstock=codstock, codproduto=codproduto, codarmazem=codarmazem,
                                   quantidade=quantidade, valor=valor, taxa=taxa, subtotal=subtotal, total=total)

                sql = "INSERT INTO stockdetalhe (codstock, codproduto, codarmazem, quantidade, valor, taxa, " \
                      "subtotal, total) values({value})".format(value=values)

            stcksql = """UPDATE stock SET taxa=taxa+{taxa}, subtotal=subtotal+{subtotal}, total=total+{total} where 
            cod = "{cod}" """.format(taxa=valortaxa, subtotal=subtotal, total=total, cod=codstock)

            try:
                self.cur.execute(sql)
                self.cur.execute(stcksql)
                self.conn.commit()

            except lite.Error as e:
                QMessageBox.critical(self, "Erro", "Os seus Dados não foram gravados. Erro: {erro} ".format(erro=e))
                return
            try:
                self.cur.execute(stcksql)
                self.conn.commit()
            except lite.Error as e:
                QMessageBox.critical(self, "Erro", "Os seus Dados não foram gravados. Erro: {erro} ".format(erro=e))
                return

            self.apagarItem.setEnabled(True)
            self.fill_table()

    def enchefornecedor(self):

        sql = "SELECT nome FROM fornecedores"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if len(data) > 0:
            for item in data:
                self.fornecedor.addItems(item)

    def encheprodutos(self):

        sql = "SELECT nome FROM produtos"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if len(data) > 0:
            for item in data:
                self.produto.addItems(item)

    def enchearmazem(self):

        sql = "SELECT nome FROM armazem"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if len(data) > 0:
            for item in data:
                self.armazem.addItems(item)

    def enchetaxas(self):

        sql = "SELECT nome FROM taxas"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if len(data) > 0:
            for item in data:
                self.taxa.addItems(item)

        self.taxa.setCurrentText("IVA")
    def closeEvent(self, evt):
        parent = self.parent()
        if parent is not None:
            parent.fill_table()

    def fechar(self):
        self.close()

    def limpar(self):
        for child in (self.findChildren(QLineEdit) or self.findChildren(QTextEdit)):
            if child.objectName() not in ["cod", "cal1", "cal2"]: child.clear()

        # gera novo codigo para stock
        from utilities import codigo
        self.cod.setText("ST" + codigo("ST" + "ABCDEF1234567890"))

    def validacaodetalhes(self):
        sql = """SELECT * from stock where cod = "{codigo}" """.format(codigo=str(self.cod.text()))

        self.cur.execute(sql)
        data = self.cur.fetchall()

        if self.quantidade.text() == 0:
            QMessageBox.information(self, "Erro de quantidade", "Quantidade deve ser maior que zero (0)")
            self.quantidade.setFocus()
            return False
        elif self.preco.text() == 0:
            QMessageBox.information(self, "Erro de valor", "Valor deve ser maior que zero (0)")
            self.valor.setFocus()
            return False
        elif len(data) == 0:
            if QMessageBox.question(self, "Erro de Documento", "Detalhes do fornecedor ainda não foram gravados."
                                                            " \n Deseja Gravar agora?") == QMessageBox.Yes:
                self.gravardoc()
                return False
        else:
            return True

    def mostrarReg(self):

        sql = """SELECT fornecedores.nome, stock.numero, stock.data, stock.valor, stock.pago, stockdetalhe.codproduto,
        stockdetalhe.codarmazem, stockdetalhe.quantidade, stockdetalhe.valor  from fornecedores INNER JOIN stock ON 
        fornecedores.cod = stock.fornecedor INNER JOIN stockdetalhe ON stock.cod=stockdetalhe.codstock
        where stock.cod = "{codigo}" """.format(codigo=str(self.cod.text()))

        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) == 0:
            self.cod.setText("ST" + cd("ABCDEF1234567890"))
        else:

            self.fornecedor.setCurrentText(''.join(data[0][0]))
            self.numerodocumento.setText(''.join(data[0][1]))
            self.datadocumento.setDate(QDate.fromString(''.join(data[0][2])))
            self.valor_documento.setValue(decimal.Decimal(data[0][3]))
            self.valor_pago.setValue(decimal.Decimal(data[0][4]))

            self.fill_table()

    def fill_data(self):
        if self.current_id == "":
            return

        sql = """ SELECT produtos.nome, armazem.nome, stockdetalhe.quantidade, 
        stockdetalhe.valor from produtos INNER JOIN stockdetalhe ON produtos.cod=stockdetalhe.codproduto INNER JOIN
        armazem ON armazem.cod=stockdetalhe.codarmazem where stockdetalhe.cod="{cod}" 
        """.format(cod=self.current_id)

        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) == 0:
            return

        self.produto.setCurrentText(''.join(data[0][0]))
        self.armazem.setCurrentText(''.join(data[0][1]))
        self.quantidade.setValue(decimal.Decimal(data[0][2]))
        self.custo.setValue(decimal.Decimal(data[0][3]))

    def existe(self, codigo):

        sql = """SELECT cod from stock where cod = "{codigo}" """.format(codigo=str(codigo))

        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) == 0:
            return False
        else:
            return True

    def existeproduto(self, codproduto, codstock):

        sql = """SELECT cod from stockdetalhe where codstock="{codstock}" and codproduto = "{codproduto}"
         """.format(codstock=str(codstock), codproduto=codproduto)

        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) == 0:
            return False
        else:
            return True

    def addRecord(self):

        if self.validacao() is True:
            sql = """select quantidade, codproduto from stockdetalhe where codstock="{cod}"
            """.format(cod=self.cod.text())
            self.cur.execute(sql)
            stockdata = self.cur.fetchall()

            if len(stockdata) == 0:
                return

            for item in stockdata:

                sql = """ UPDATE produtos set quantidade=quantidade+{qty} where cod="{cod}" """.format(qty=item[0],cod=item[1])
                self.cur.execute(sql)

            if QMessageBox.question(self, "Gravar dados", "Esta acção vai actualizar quantidades de stock e não poderá"
                                                          " ser revertida. \n Deseja Continuar?") == QMessageBox.Yes:

                sql = """ UPDATE stock set estado="completo" where cod="{cod}" """.format(cod=self.cod.text())
                self.cur.execute(sql)

                try:
                    self.conn.commit()
                    self.close()
                except lite.Error as e:
                    QMessageBox.information(self, "Erro", "Erro ao actualizar quantiades. Erro: {erro}".format(erro=e))

    def connect_db(self):
        # Connect to database and retrieves data
        try:
            self.conn = lite.connect(filename)
            self.cur = self.conn.cursor()

        except lite.Error as e:
            QMessageBox.critical(self, "Erro ao conectar a Base de Dados",
                                 "Os seus Dados não foram gravados. Erro: {erro} ".format(erro=e))
            sys.exit(True)

    def removerow(self):

        if self.current_id == "":
            QMessageBox.information(self, "Info", "Seleccione o registo a apagar na tabela")
            return

        sql = """delete from stockdetalhe where cod = "{codigo}" """.format(codigo=str(self.current_id))
        self.cur.execute(sql)
        self.conn.commit()
        self.fill_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    helloPythonWidget = Cliente()
    helloPythonWidget.show()

    sys.exit(app.exec_())