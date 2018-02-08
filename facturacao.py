# -*- coding: latin-1 -*-
"""
Created on Fri Mar 02 23:18:43 2012

@author: lims
"""
import sys
import datetime
import decimal

from PyQt5.QtWidgets import (QLabel, QLineEdit,QVBoxLayout, QToolBar, QMessageBox, QAbstractButton, \
    QTextEdit, QAction, QApplication, QGroupBox, QPushButton, QComboBox, QMainWindow, QCalendarWidget,\
    QHBoxLayout, QWidget, QTableView, QCheckBox, QAbstractItemView, QSplitter, QDialog, QGridLayout)

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QFont

import sqlite3 as lite
from extenso import dExtenso as Extenso

from sortmodel import MyTableModel
from utilities import codigo as cd
from pricespinbox import price
from database import DBCOnnection

from documentos import Cliente as doc
from produtos import produto as prod
from taxas import Cliente as tx
from clientes import Cliente as cl
filename = "dados.tsdb"

today = datetime.date.today()
year = today.year
day = today.day
month = today.month
documentos_protegidos = ["Factura", "Recibo", "Cotacão", "VD"]
class Cliente(QMainWindow):
    def __init__(self, parent=None):
        super(Cliente, self).__init__(parent)

        self.user = ""
        
        self.codigogeral = "FT" + cd("FT" + "ABCDEF1234567890")
        self.codcliente = ""
        self.codproduto = ""
        self.coddocumento = ""
        self.custoproduto = 0.00
        self.valortaxa = 0.00
        self.current_id = ""
        
        self.accoes()
        self.ui()

        if self.parent() is None:
            self.db = self.connect_db()
        else:
            self.cur = self.parent().cur
            self.conn = self.parent().conn

        self.encheprodutos()
        self.encheclientes()
        self.enchedocumentos()
        self.enchetaxa()

    def ui(self):

        self.titulo = QLabel("000,000,000.00")
        self.titulo.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        boldFont = QFont('Consolas', 42)
        boldFont.setBold(True)
        self.titulo.setFont(boldFont)

        clientegrupo = QGroupBox("Detalhes do Cliente")
        clientegrupo.setMaximumHeight(70)
        documentogrupo = QGroupBox("Detalhes do Documento(Escolha Cliente)")
        documentogrupo.setMaximumHeight(70)
        detalhesgrupo = QGroupBox("Detalhes de Items")

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

        self.butao_adicionarnalista = QPushButton("Adicionar na Lista")
        self.butao_gravardetalhe = QPushButton("Gravar Detalhes")
        self.butao_gravardetalhe.setMaximumWidth(120)
        self.butao_gravardetalhe.setMinimumWidth(120)
        self.butao_gravardetalhe.clicked.connect(self.addRecord)
        self.butao_apagarItem = QPushButton(QIcon("./icons/remove.ico"), "Eliminar Linha")
        self.butao_apagarItem.setMaximumWidth(120)
        self.butao_apagarItem.setMinimumWidth(120)
        # self.butao_apagarItem.clicked.connect(self.removerow)
        self.butao_apagarItem.setEnabled(False)

        documento = QLabel("Documento")
        documento.setMinimumWidth(100)
        cliente = QLabel("Cliente")
        cliente.setMinimumWidth(100)

        self.combo_documento = QComboBox()
        self.combo_documento.currentTextChanged.connect(self.getcoddocumento)
        self.combo_documento.setEditable(True)
        self.combo_cliente = QComboBox()
        self.combo_cliente.currentTextChanged.connect(self.getcodcliente)
        self.combo_cliente.setEditable(True)
        self.butao_gravarcliente = QPushButton(QIcon("./icons/add.ico"), "Adicionar Cliente")
        self.butao_gravarcliente.clicked.connect(self.gravacliente)
        self.butao_gravarcliente.setMaximumWidth(120)
        self.butao_gravarcliente.setMinimumWidth(120)
        self.butao_gravardocumento = QPushButton(QIcon("./icons/add.ico"), "Adicionar Documento")
        self.butao_gravardocumento.clicked.connect(self.gravadocumento)
        self.butao_gravardocumento.setMaximumWidth(120)
        self.butao_gravardocumento.setMinimumWidth(120)

        codigo = QLabel("Código/Código de Barras")
        descriccao = QLabel("Descrição")
        descriccao.setMinimumWidth(100)
        preco = QLabel("Preço")
        quantidade = QLabel("Quantidade")
        taxa = QLabel("Taxa")
        desconto = QLabel("Desconto")
        extenso = QLabel("Valor por extenso")
        notas = QLabel("Notas")
        
        self.codigoproduto = QLineEdit()
        self.codigoproduto.textChanged.connect(self.getnomeproduto)
        self.combo_produto = QComboBox()
        self.combo_produto.setEditable(True)
        self.combo_produto.currentTextChanged.connect(self.getcodproduto)
        self.butao_produto = QPushButton(QIcon("./icons/add.ico"), "Adicionar Item")
        self.butao_produto.clicked.connect(self.gravaproduto)
        self.preco = price()
        self.preco.setRange(0.00, 999999999999.99)
        self.quantidade = price()
        self.quantidade.setRange(0.00, 999999999999.99)
        self.quantidade.setSingleStep(1.00)
        self.desconto = price()
        self.desconto.setRange(0.00, 99.99)
        self.desconto.setSingleStep(1.00)
        self.combo_taxa = QComboBox()
        self.combo_taxa.setEditable(True)
        self.combo_taxa.currentTextChanged.connect(self.getcodtaxa)
        self.taxabutton = QPushButton(QIcon("./icons/save.ico"), "Adiccionar Taxa")
        self.taxabutton.clicked.connect(self.gravataxa)
        self.taxa = QCheckBox("Incluir TAXA no Preço")
        self.taxa.setChecked(True)
        self.extenso = QLineEdit()
        self.obs = QTextEdit()

        ly = QGridLayout()
        ly.addWidget(codigo, 0, 0)
        ly.addWidget(self.codigoproduto, 0, 1)
        ly.addWidget(descriccao, 1, 0,)
        ly.addWidget(self.combo_produto, 1, 1, 1, 5)
        ly.addWidget(self.butao_produto, 1, 6)
        ly.addWidget(preco, 2, 0)
        ly.addWidget(self.preco, 2, 1)
        ly.addWidget(quantidade, 3, 0)
        ly.addWidget(self.quantidade, 3, 1)
        ly.addWidget(taxa, 4, 0)
        ly.addWidget(self.combo_taxa, 4, 1)
        ly.addWidget(self.taxabutton, 4, 2)
        ly.addWidget(self.taxa, 4, 3, 1, 3)
        ly.addWidget(desconto, 5, 0)
        ly.addWidget(self.desconto, 5, 1)
        ly.addWidget(extenso, 6, 0)
        ly.addWidget(self.extenso, 6, 1, 1, 6)
        ly.addWidget(notas, 7, 0)
        ly.addWidget(self.obs, 7, 1, 1, 6)
        ly.addWidget(self.butao_gravardetalhe, 8, 5)
        ly.addWidget(self.butao_apagarItem, 8, 6)
        detalhesgrupo.setLayout(ly)

        documentoLayout = QGridLayout()
        documentoLayout.addWidget(documento, 0, 0)
        documentoLayout.addWidget(self.combo_documento, 0, 1, 1, 5)
        documentoLayout.addWidget(self.butao_gravardocumento, 0, 7)

        documentogrupo.setLayout(documentoLayout)

        clientelayout = QGridLayout()
        clientelayout.addWidget(cliente, 0, 0)
        clientelayout.addWidget(self.combo_cliente, 0, 1, 1, 5)
        clientelayout.addWidget(self.butao_gravarcliente, 0, 7)

        clientegrupo.setLayout(clientelayout)

        controlslayout = QVBoxLayout()
        controlslayout.addWidget(documentogrupo)
        controlslayout.addWidget(clientegrupo)
        controlslayout.addWidget(detalhesgrupo)

        splitter = QSplitter(Qt.Horizontal)
        controlswidget = QGroupBox()

        controlswidget.setLayout(controlslayout)

        splitter.addWidget(controlswidget)
        splitter.addWidget(self.tabela)

        mainlayout = QVBoxLayout()

        produtowidget = QWidget()

        # produtowidget.setLayout(ly)

        headerlayout = QHBoxLayout()
        headerlayout.addWidget(produtowidget)
        headerlayout.addWidget(self.titulo)

        # Layout de Produtos, Normalmente deve ser flowlayout
        self.combo_produtoslayout = QHBoxLayout()

        #Layout da Familia de produtos, estara por cima de todos
        self.familialayout = QHBoxLayout()

        # Layout de Subfalilias a esquerda e Produtos a direita
        self.subfamilialayout = QVBoxLayout()
        subbuttonslayout = QHBoxLayout()
        subbuttonslayout.addLayout(self.subfamilialayout)
        subbuttonslayout.addLayout(self.combo_produtoslayout)

        buttonslayout = QVBoxLayout()
        buttonslayout.addLayout(self.familialayout)
        buttonslayout.addLayout(subbuttonslayout)

        controlswidget.setLayout(buttonslayout)

        headerWidget = QGroupBox()
        headerWidget.setMaximumHeight(80)

        headerWidget.setLayout(headerlayout)

        mainlayout.addWidget(headerWidget)
        mainlayout.addWidget(splitter)
        mainlayout.addWidget(self.tool)

        centralwidget = QWidget()
        centralwidget.setLayout(mainlayout)
        self.setCentralWidget(centralwidget)

        self.setWindowTitle("Facturação")

    def keyPressEvent(self, event):
        if Qt.Key_Enter and self.codigoproduto.hasFocus() is True:
            self.addRecord()

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

    # Actualiza a tabela ou lista de Items
    def fill_table(self):

        header = ["cod", "Documento", "Descrição", "Armazém", "Quantidade", "Preço", "Taxa", "SubTotal", "Total"]

        sql = """ select stockdetalhe.cod, codstock, produtos.nome, documento.nome, stockdetalhe.quantidade, 
        stockdetalhe.valor, stockdetalhe.taxa, stockdetalhe.subtotal, stockdetalhe.total from produtos INNER JOIN
        stockdetalhe ON produtos.cod=stockdetalhe.codproduto INNER JOIN documento ON documento.cod=stockdetalhe.coddocumento 
        where codstock="{codstock}" """.format(codstock=self.cod.text())

        self.cur.execute(sql)
        data = self.cur.fetchall()
        self.tabledata = data

        if len(data) == 0:
            self.butao_apagarItem.setEnabled(False)
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

    # Enche a combobox produtos com Lista de Produtos
    def encheprodutos(self):

        self.combo_produto.clear()

        sql = """SELECT nome FROM produtos"""
        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) > 0:
            for item in data:
                self.combo_produto.addItems(item)

    # Enche a combobox clientes com Lista de clientes
    def encheclientes(self):

        self.combo_cliente.clear()

        sql = """SELECT nome FROM clientes"""
        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) > 0:
            for item in data:
                self.combo_cliente.addItems(item)

    # Enche a combobox documento com Lista de documentos
    def enchedocumentos(self):

        self.combo_documento.clear()

        sql = """SELECT nome FROM documentos"""
        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) > 0:
            for item in data:
                self.combo_documento.addItems(item)

    # Enche a combobox taxas com Lista de taxas
    def enchetaxa(self):

        self.combo_taxa.clear()

        sql = """SELECT nome FROM taxas"""
        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) > 0:
            for item in data:
                self.combo_taxa.addItems(item)
                self.combo_taxa.setCurrentText("IVA")

    # Acontence quando clicas o tabela
    def clickedSlot(self, index):

        self.row = int(index.row())

        self.col = int(index.column())

        indice= self.tm.index(self.row, 0)
        self.current_id = indice.data()

        self.fill_data()

        self.butao_apagarItem.setEnabled(True)

    # Busca o codigo do cliente baseando no cliente seleccionado
    def getcodcliente(self):
        sql = """select cod from clientes where nome= "{nome}" """.format(nome=self.combo_cliente.currentText())

        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) > 0:
            self.codcliente = "".join(data[0])
        else:
            self.codcliente = ""

    # Busca o codigo da taxa baseando na taxa seleccionado
    def getcodtaxa(self):
        sql = """select cod from taxas where nome= "{nome}" """.format(nome=self.combo_taxa.currentText())

        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) > 0 :
            self.codtaxas = "".join(data[0])
            self.getvalortaxa(self.combo_taxa.currentText())
        else:
            self.codtaxas = ""

    # Busca o codigo do produto baseando no produto seleccionado
    def getcodproduto(self):
        sql = """select cod, preco, custo from produtos where nome= "{nome}" """.format(nome=self.combo_produto.currentText())

        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) > 0:
            self.codproduto = "".join(data[0][0])
            self.preco.setValue(float(data[0][1]))
            self.custoproduto = float(data[0][2])
            self.codigoproduto.setText(self.codproduto)
        else:
            self.codproduto = ""
            self.custoproduto = 0.00

            # Busca o codigo do produto baseando no produto seleccionado

    def getnomeproduto(self):
        sql = """select cod, preco, custo, nome from produtos where cod= "{cod}" """.format(cod=self.codigoproduto.text())

        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) > 0:
            self.codproduto = "".join(data[0][0])
            self.preco.setValue(float(data[0][1]))
            self.custoproduto = float(data[0][2])
            self.combo_produto.setCurrentText("".join(data[0][3]))
        else:
            self.codproduto = ""
            self.custoproduto = 0.00

    # Busca o codigo do documento baseando no documento seleccionado
    def getcoddocumento(self):
        sql = """select cod from documentos where nome= "{nome}" """.format(nome=self.combo_documento.currentText())

        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) > 0:
            self.coddocumento = "".join(data[0])
        else:
            self.coddocumento = ""

    # Busca o valor da taxa baseando no nome seleccionado
    def getvalortaxa(self, nome):
        sql = """select valor from taxas where nome= "{nome}" """.format(nome=nome)

        self.cur.execute(sql)
        data = self.cur.fetchall()
        if len(data) > 0:
            for item in data[0]:
                self.valortaxa = float(item)
        else:
            self.valortaxa = 0.00

    #
    def habilitarcliente(self):
        self.gravar_cliente.setEnabled(True)
        self.desabilitarcliente()
        self.ativar_cliente.setEnabled(False)

    def desabilitarcliente(self):

        self.combo_cliente.setEnabled(not self.combo_cliente.isEnabled())
        self.numerodocumento.setEnabled(not self.numerodocumento.isEnabled())
        self.datadocumento.setEnabled(not self.datadocumento.isEnabled())
        self.valor_pago.setEnabled(not self.valor_pago.isEnabled())
        self.valor_documento.setEnabled(not self.valor_documento.isEnabled())

    def enchecliente(self):

        sql = "SELECT nome FROM clientees"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if len(data) > 0:
            for item in data:
                self.combo_cliente.addItems(item)

    def closeEvent(self, event):
        parent = self.parent()
        try:
            if parent is not None:
                parent.fill_table()
        except:
            return

    def fechar(self):
        self.close()

    def limpar(self):
        for child in (self.findChildren(QLineEdit) or self.findChildren(QTextEdit)):
            if child.objectName() not in ["cod", "cal1", "cal2"]: child.clear()

        # gera novo codigo para stock
        from utilities import codigo
        self.cod.setText("DC" + codigo("DC" + "ABCDEF1234567890"))

    def validacaodetalhes(self):

        if self.quantidade.value() == 0.00:
            QMessageBox.information(self, "Erro de quantidade", "Quantidade deve ser maior que zero (0)")
            self.quantidade.setFocus()
            return False
        elif self.preco.value() <= self.desconto.value():
            QMessageBox.information(self, "Erro de valor", "Preço deve ser que o desconto")
            self.preco.setFocus()
            return False
        elif self.preco.value() == 0.00:
            QMessageBox.information(self, "Erro de valor", "Preço deve ser maior que zero (0)")
            self.preco.setFocus()
            return False
        elif self.combo_cliente.currentText() == "" or self.codcliente == "":
            QMessageBox.information(self, "Erro de Cliente", "Escolha o nome do cliente ou "
                                                             "grave novo no Dialogo asseguir")
            self.combo_cliente.setFocus()
            self.gravacliente()
            return False
        elif self.combo_documento.currentText() == "" or self.coddocumento == "":
            QMessageBox.information(self, "Erro de documento", "Escolha ou entre o Tipo de Documento ou "
                                                               "Grave novo no dialogo asseguir")
            self.combo_documento.setFocus()
            self.gravadocumento()
            return False
        elif self.combo_taxa.currentText() == "" or self.codtaxas == "":
            QMessageBox.information(self, "Erro de Taxa", "Entre a Taxa")
            self.combo_taxa.setFocus()
            return False
        elif self.combo_produto.currentText() == "" or self.codproduto == "":
            QMessageBox.information(self, "Erro de Produto/Serviço", "Entre o Produto/Serviço")
            self.combo_produto.setFocus()
            return False
        else:
            self.combo_cliente.setEnabled(False)
            self.combo_documento.setEnabled(False)
            return True

    def mostrarReg(self):

        sql = """SELECT clientees.nome, stock.numero, stock.data, stock.valor, stock.pago, stockdetalhe.codproduto,
        stockdetalhe.coddocumento, stockdetalhe.quantidade, stockdetalhe.valor  from clientees INNER JOIN stock ON 
        clientees.cod = stock.cliente INNER JOIN stockdetalhe ON stock.cod=stockdetalhe.codstock
        where stock.cod = "{codigo}" """.format(codigo=str(self.cod.text()))

        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) == 0:
            self.cod.setText("DC" + cd("ABCDEF1234567890"))
        else:

            self.combo_cliente.setCurrentText(''.join(data[0][0]))
            self.numerodocumento.setText(''.join(data[0][1]))
            self.datadocumento.setDate(QDate.fromString(''.join(data[0][2])))
            self.valor_documento.setValue(float(data[0][3]))
            self.valor_pago.setValue(float(data[0][4]))

            self.fill_table()

    def fill_data(self):
        if self.current_id == "":
            return

        sql = """ SELECT produtos.nome, documento.nome, stockdetalhe.quantidade, 
        stockdetalhe.valor from produtos INNER JOIN stockdetalhe ON produtos.cod=stockdetalhe.codproduto INNER JOIN
        documento ON documento.cod=stockdetalhe.coddocumento where stockdetalhe.cod="{cod}" 
        """.format(cod=self.current_id)

        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) == 0:
            return

        self.combo_produto.setCurrentText(''.join(data[0][0]))
        self.combo_documento.setCurrentText(''.join(data[0][1]))
        self.quantidade.setValue(float(data[0][2]))
        self.custo.setValue(float(data[0][3]))

    def existe(self, codigo):

        sql = """SELECT cod from facturacao where cod = "{codigo}" """.format(codigo=str(codigo))

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

    def incrimenta(self, ano, coddocumento):
        sql = """select max(numero) from facturacao where ano={ano} and 
        coddocumento="{coddoc}" """.format(ano=ano, coddoc=coddocumento)

        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
        except lite.Error as e:
            print(e)
            return

        if data[0][0] is None:
            self.numero = 1
        else:
            self.numero = data[0][0] + 1

    # Metodo que grava documento caso nao exista
    def verifica_documentos(self):

        sql = """ SELECT cod from documentos where cod={cod}""".format(cod=self.coddocumento)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if len(data) == 0:
            if QMessageBox.information(self, "Documento nao existe",
                                       "Documento não existe. Grave no dialogo asseguir.") == QMessageBox.Ok:
                self.gravadocumento()
            return False
        else:
            return True

    # Metodo que verifica a existencia do cliente na Base de Dados
    def verifica_clientes(self):

        sql = """ SELECT cod from clientes where cod={cod}""".format(cod=self.codcliente)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if len(data) == 0:
            if QMessageBox.information(self, "Cliente não existe",
                                       "Cliente não existe. Grave no dialogo asseguir.") == QMessageBox.Ok:
                self.gravacliente()

            return False
        else:
            return True

    def addRecord(self):

        self.incrimenta(year, self.coddocumento)

        if self.validacaodetalhes() is True:

            valortaxa = self.valortaxa / 100
            code = self.codigogeral
            numero = self.numero
            coddocumento = self.coddocumento
            codcliente = self.codcliente
            data = QDate.currentDate().toString()
            custo = self.custoproduto * self.quantidade.value()
            desconto = self.desconto.value() / 100
            valordeconto = float(self.quantidade.value() * self.preco.value()) * desconto

            if self.taxa.isChecked() is True:
                subtotal = float(self.quantidade.value() * self.preco.value()) - valordeconto
            else:
                subtotal = float((self.quantidade.value() * self.preco.value()) - valordeconto) / (1 + valortaxa)

            taxa = valortaxa * float(self.quantidade.value() * self.preco.value())
            total = subtotal + taxa
            lucro = subtotal - custo
            pago = 0.00
            troco = 0.00
            banco = 0.00
            cash = 0.00
            tranferencia = 0.00
            estado = 1
            extenso = ""
            ano = year
            mes = month
            obs = self.obs.toPlainText()
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

            print("gravar")

            if self.existe(self.codigogeral) is True:

                print(code, custo, subtotal, valordeconto, taxa, total, lucro)

                sql = """UPDATE facturacao set custo=custo+{custo}, subtotal=subtotal+{subtotal}, 
                desconto=desconto+{desconto}, taxa=taxa+{taxa}, total=total+{total}, lucro=lucro+{lucro} 
                where cod="{cod}" """.format(cod=code, custo=custo, subtotal=subtotal, desconto=valordeconto,
                                            taxa=taxa, total=total, lucro=lucro)
            else:

                values = """ "{cod}", {numero}, "{coddocumento}", "{codcliente}", "{data}", {custo}, {subtotal}, 
                {desconto}, {taxa}, {total}, {lucro}, {pago}, {troco}, {banco}, {cash}, {tranferencia}, {estado}, 
                {ano}, {mes}, "{obs}", "{created}", "{modified}", "{modified_by}", "{created_by}"
                 """.format(cod=code, numero=numero, coddocumento=coddocumento, codcliente=codcliente,
                            data=data, custo=custo, subtotal=subtotal, desconto=valordeconto, taxa=taxa,
                            total = total, lucro = lucro, pago = pago, troco=troco, banco=banco,
                            cash=cash, tranferencia=tranferencia, estado=estado,ano=ano,
                            mes=mes, obs=obs, created=created, modified=modified, modified_by=modified_by,
                            created_by=created_by)

                print(values)
                sql = """ INSERT INTO facturacao (cod, numero, coddocumento ,codcliente, data, custo, subtotal,
                 desconto, taxa, total,  lucro, pago , troco, banco, cash, tranferencia, estado, ano, mes, 
                 obs, created, modified, modified_by, created_by) values({value})""".format(value=values)

                sql2 = """INSERT INTO facturacaodetalhe """
            try:
                print(sql)
                self.cur.execute(sql)
                self.conn.commit()
            except lite.Error as e:
                QMessageBox.critical(self, "Erro", "Os seus Dados não foram gravados. Erro: {erro} ".format(erro=e))
                return

            self.titulo.setText(str(total))
            # self.limpar()
            # self.fill_table()

    def gravadetalhes(self, codfacturacao, codproduto, custo, preco, quantidade, subtotal,
                      desconto, taxa, total, lucro):

        values = """{codfacturacao}, {codproduto}, {custo}, {preco}, {quantidade}, {subtotal}, {desconto}, {taxa}, 
        {total}, {lucro}""".format(codfacturacao=codfacturacao, codproduto=codproduto, custo=custo, preco=preco,
quantidade=quantidade, subtotal=subtotal, desconto=desconto, taxa=taxa , total=total, lucro=lucro)

        sql = """INSERT INTO (facturadetalhe codfacturacao, codproduto, custo, preco, quantidade, desconto, 
        subtotal, total, lucro) values({values}) """.format(values=values)
        subtotal = preco * quantidade
        total = ""
        lucro = ""

    def gravadetalhe(self):
        if self.validacaodetalhes() is True:

            valortaxa = self.valortaxa / 100
            code = self.codigogeral
            numero = 1
            coddocumento = self.coddocumento
            codcliente = self.codcliente
            data = QDate.currentDate().toString()
            custo = self.custoproduto * self.quantidade.value()
            desconto = self.desconto.value() / 100
            valordeconto = float(self.quantidade.value() * self.preco.value()) * desconto

            if self.taxa.isChecked() is True:
                subtotal = float(self.quantidade.value() * self.preco.value()) - valordeconto
            else:
                subtotal = float((self.quantidade.value() * self.preco.value()) - valordeconto) / (1 + valortaxa)

            taxa = valortaxa * float(self.quantidade.value() * self.preco.value())
            total = subtotal + taxa
            lucro = subtotal - custo
            pago = 0.00
            troco = 0.00
            banco = 0.00
            cash = 0.00
            tranferencia = 0.00
            estado = 1
            extenso = ""
            ano = year
            mes = month
            obs = self.obs.toPlainText()
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

            print("gravar")

            if self.existe(self.codigogeral) is True:

                print(code, custo, subtotal, valordeconto, taxa, total, lucro)

                sql = """UPDATE facturacao set custo=custo+{custo}, subtotal=subtotal+{subtotal}, 
                       desconto=desconto+{desconto}, taxa=taxa+{taxa}, total=total+{total}, lucro=lucro+{lucro} 
                       where cod="{cod}" """.format(cod=code, custo=custo, subtotal=subtotal, desconto=valordeconto,
                                                    taxa=taxa, total=total, lucro=lucro)
            else:

                values = """ "{cod}", {numero}, "{coddocumento}", "{codcliente}", "{data}", {custo}, {subtotal}, 
                       {desconto}, {taxa}, {total}, {lucro}, {pago}, {troco}, {banco}, {cash}, {tranferencia}, {estado}, 
                       {ano}, {mes}, "{obs}", "{created}", "{modified}", "{modified_by}", "{created_by}"
                        """.format(cod=code, numero=numero, coddocumento=coddocumento, codcliente=codcliente,
                                   data=data, custo=custo, subtotal=subtotal, desconto=valordeconto, taxa=taxa,
                                   total=total, lucro=lucro, pago=pago, troco=troco, banco=banco,
                                   cash=cash, tranferencia=tranferencia, estado=estado, ano=ano,
                                   mes=mes, obs=obs, created=created, modified=modified, modified_by=modified_by,
                                   created_by=created_by)

                print(values)
                sql = """ INSERT INTO facturacao (cod, numero, coddocumento ,codcliente, data, custo, subtotal,
                        desconto, taxa, total,  lucro, pago , troco, banco, cash, tranferencia, estado, ano, mes, 
                        obs, created, modified, modified_by, created_by) values({value})""".format(value=values)
            try:
                print(sql)
                self.cur.execute(sql)
                self.conn.commit()
            except lite.Error as e:
                QMessageBox.critical(self, "Erro", "Os seus Dados não foram gravados. Erro: {erro} ".format(erro=e))
                return

    def connect_db(self):
        # Connect to database and retrieves data
        try:
            self.conn = lite.connect(filename)
            self.conn.execute("pragma foreign_keys=ON")
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

    def gravadocumento(self):

        cl = doc(self)
        if self.coddocumento == "":
            cl.nome.setText(self.combo_documento.currentText())
        else:
            cl.cod.setText(self.coddocumento)

        cl.mostrarReg()
        cl.setModal(True)
        cl.show()

    def gravacliente(self):

        cli = cl(self)
        if self.codcliente == "":
            cli.nome.setText(self.combo_cliente.currentText())
        else:
            cli.cod.setText(self.codcliente)

        cli.mostrarReg()
        cli.setModal(True)
        cli.show()

    def gravataxa(self):

        cl = tx(self)
        if self.codtaxas == "":
            cl.nome.setText(self.combo_taxa.currentText())
        cl.cod.setText(self.codtaxas)
        cl.mostrarReg()
        cl.setModal(True)
        cl.show()

    def gravaproduto(self):
        print(type(self.combo_produto.currentText()))

        cl = prod(self)
        if self.codproduto == "":
            cl.nome.setPlainText(str(self.combo_produto.currentText()))
        else:
            cl.cod.setText(self.codproduto)
        cl.mostrarReg()
        cl.setModal(True)
        cl.show()

    def enterEvent(self, evt):
        self.getcodtaxa()
        self.getcodcliente()
        self.getcoddocumento()
        self.getcodproduto()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    helloPythonWidget = Cliente()
    helloPythonWidget.show()

    sys.exit(app.exec_())