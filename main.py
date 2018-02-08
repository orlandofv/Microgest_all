# -*- coding: latin-1 -*-

import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QTabWidget, QStatusBar, \
    QAction, QToolBar, QMenuBar, QToolBox, QVBoxLayout, QFrame, QCommandLinkButton, QGroupBox, \
    QCalendarWidget, QLabel, qApp, QMessageBox, QStyleFactory
import sqlite3 as lite
import login

DARK_BLUE = "./Styles/dark-blue.qss"
DARK_GREEN = "./Styles/dark-green.qss"
DARK_ORANGE = "./Styles/dark-orange.qss"
LIGHT_BLUE = "./Styles/light-blue.qss"
LIGHT_GREEN = "./Styles/light-green.qss"
LIGHT_ORANGE = "./Styles/light-orange.qss"

filename = "dados.tsdb"

class Gestor(QMainWindow):
    
    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)

        if self.parent() is None:
            self.db = self.connect_db()
        else:
            self.conn = self.parent().conn
            self.cur = self.parent().cur

        self.user = ""

        self.ui()
        # self.accoes()

        self.adduser()


        Login = login.Login(self)
        Login.setModal(True)
        Login.show()

    def stylesheet(self, file):
        print(file)
        try:
            FICHEIRO = open(file, 'r')
            STYLE = FICHEIRO.read()
            self.setStyleSheet(STYLE)
        except FileNotFoundError as e:
            QMessageBox.warning(self, "Ficheiro não encontrado", "Ficheiro não existe")
            return

    def ui(self):
        

        self.tab = QTabWidget()
        self.tab.setTabsClosable(True)
        self.tab.setTabPosition(1)
        self.tab.setMovable(True)
        self.tab.tabCloseRequested.connect(self.tabClose)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.setCentralWidget(self.tab)

    def adduser(self):

        import startpage
        sp = startpage.startPage(self)
        self.tab.addTab(sp, "Bem Vindo")

    def accoes(self):
        self.painel = QDockWidget("Painel", self)
        self.painel.setContentsMargins(0, 0, 0, 0)
        self.painel.setAllowedAreas(Qt.LeftDockWidgetArea |
                                    Qt.RightDockWidgetArea)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.painel)

        familias = QAction(QIcon("./icons/familias.jpg"), "Lista de Famílias de Items",self)
        subfamilias = QAction(QIcon("./icons/subfamilias.jpg"), "Lista de Sub Famílias de Items", self)
        produtos = QAction(QIcon("./icons/produtos.png"), "Lista de Produtos/Serviços", self)
        armazens = QAction(QIcon("./icons/armazens.jpg"), "Lista de Armazéns", self)
        stock = QAction(QIcon("./icons/stock.jpg"), "Lista de Stock", self)

        clientes = QAction(QIcon("./icons/clientes.ico"), "Lista de Clientes", self)
        fornecedores = QAction(QIcon("./icons/fornecedores.ico"), "Lista de Fornecedores",self)

        taxas = QAction(QIcon("./icons/taxas.png"), "Lista de Taxas", self)
        documentos = QAction(QIcon("./icons/documentos.jpg"), "Lista de Documentos", self)

        users = QAction(QIcon("./icons/users.ico"), "Lista de Usuários",self)
        configuracoes = QAction(QIcon("./icons/cofiguracao.ico"), "Configurações",self)

        darkblue = QAction("Dark Blue", self)
        darkgreen = QAction("Dark Green", self)
        darkorange = QAction("Dark Orange", self)
        lightblue = QAction("Light Blue", self)
        lightgreen = QAction("Light Green", self)
        lightorange = QAction("Light Orange", self)

        darkblue.triggered.connect(lambda: self.styleSheet(DARK_BLUE))
        darkgreen.triggered.connect(lambda: self.styleSheet(DARK_GREEN))
        darkorange.triggered.connect(lambda: self.styleSheet(DARK_ORANGE))
        lightblue.triggered.connect(lambda: self.styleSheet(DARK_BLUE))
        lightgreen.triggered.connect(lambda: self.styleSheet(LIGHT_GREEN))
        lightorange.triggered.connect(lambda: self.styleSheet(LIGHT_ORANGE))

        tool = QToolBar()
        tool.setWindowTitle("Barra de Ferramentas")

        tool.setAllowedAreas(Qt.TopToolBarArea|
        Qt.BottomToolBarArea)
        self.addToolBar(tool)

        tool.addAction(familias)
        tool.addAction(subfamilias)
        tool.addAction(produtos)
        tool.addAction(armazens)
        tool.addAction(stock)
        tool.addSeparator()
        tool.addAction(clientes)
        tool.addAction(fornecedores)
        tool.addSeparator()
        tool.addAction(taxas)
        tool.addAction(documentos)
        tool.addSeparator()
        tool.addAction(users)
        tool.addAction(configuracoes)

        self.menu = QMenuBar()
        novoProduto = self.menu.addMenu("&Listagem")

        novoProduto.addAction(familias)
        novoProduto.addAction(subfamilias)
        novoProduto.addAction(produtos)
        novoProduto.addAction(armazens)
        novoProduto.addAction(stock)
        novoProduto.addSeparator()
        novoProduto.addAction(clientes)
        novoProduto.addAction(fornecedores)
        novoProduto.addSeparator()
        novoProduto.addAction(taxas)
        novoProduto.addAction(documentos)
        novoProduto.addSeparator()
        novoProduto.addAction(users)
        novoProduto.addAction(configuracoes)

        plastique = QAction(QIcon("./icons/hotel.png"), "Plastique",self)
        cde = QAction(QIcon("./icons/hotel.png"), "CDE",self)
        motif = QAction(QIcon("./icons/hotel.png"), "Motif",self)
        sgi = QAction(QIcon("./icons/hotel.png"), "Sgi",self)
        windows = QAction(QIcon("./icons/hotel.png"), "Windows",self)
        cleanlooks = QAction(QIcon("./icons/hotel.png"), "Cleanlooks",self)

        styleMenu = self.menu.addMenu("&Temas")
        styleMenu.addAction(darkorange)
        styleMenu.addAction(darkgreen)
        styleMenu.addAction(darkblue)
        styleMenu.addAction(lightorange)
        styleMenu.addAction(lightgreen)
        styleMenu.addAction(lightblue)
        
        styleMenu.addAction(plastique)
        styleMenu.addAction(cde)
        styleMenu.addAction(motif)
        styleMenu.addAction(sgi)
        styleMenu.addAction(windows)
        styleMenu.addAction(cleanlooks)

        self.setMenuBar(self.menu)

        toolbox = QToolBox()

        lay = QVBoxLayout()
        lay.setSpacing(0)
        widget = QFrame()

        clientesButton = QCommandLinkButton("Lista de Clientes")
        fornecedoresButton = QCommandLinkButton("Lista de fornecedores")

        clientesButton.addAction(clientes)
        lay.addWidget(clientesButton)

        fornecedoresButton.addAction(fornecedores)
        lay.addWidget(fornecedoresButton)
        lay.addStretch()

        widget.setLayout(lay)
        wid = QGroupBox()

        cal = QCalendarWidget()

        self.data = QLabel()
        font = QFont("Arial",14)
        self.data.setFont(font)

        layW = QVBoxLayout()

        user = QLabel("")
        pc = QLabel("")
        pc_user = QLabel("")
        user.setText("Usuário: %s " % self.user)
        user.setAlignment(Qt.AlignBottom)

        font = QFont("times new roman", 10)
        user.setFont(font)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        dic = os.environ
        #
        cp = dic['COMPUTERNAME']
        pu = dic['USERNAME']
        #
        pc.setText("Computador: %s " % cp)
        pc_user.setText("Usuário do PC: %s " % pu)
        pc.setFont(font)
        pc_user.setFont(font)

        layW.addWidget(self.data)
        layW.addStretch()
        layW.addStretch()
        layW.addStretch()
        layW.addStretch()
        layW.addStretch()
        layW.addStretch()
        layW.addStretch()
        layW.addStretch()
        layW.addWidget(user)
        layW.addWidget(pc)
        layW.addWidget(pc_user)

        timer = QTimer(self)
        timer.timeout.connect(self.horas)
        timer.start(1000)
        #
        layW.addStretch()
        wid.setLayout(layW)
        #
        frame = QGroupBox()
        #
        toolbox.addItem(wid,"Informação do Sistema")
        toolbox.addItem(frame,"Atalhos")

        self.painel.setWidget(toolbox)

        clientes.triggered.connect(self.listaclientes)
        fornecedores.triggered.connect(self.listafornecedores)
        users.triggered.connect(self.listausers)
        familias.triggered.connect(self.listafamilias)
        subfamilias.triggered.connect(self.listasubfamilias)
        produtos.triggered.connect(self.listaprodutos)
        armazens.triggered.connect(self.listaarmazems)
        taxas.triggered.connect(self.listataxas)
        stock.triggered.connect(self.listastock)
        documentos.triggered.connect(self.listadocumentos)

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

    def horas(self):
        self.data.setText(QDate.currentDate().toString("dd-MM-yyyy") + "  " + QTime.currentTime().toString())
        # self.ac.setTime(QTime.currentTime())

    def menuVisible(self):
        self.menu.setVisible(True)

    def dadosEmp(self):
        setings = QSettings()
        self.nome = setings.value("empresa/nome").toString()
        self.cabecalho = setings.value("empresa/cabecalho").toString()
        self.logo = setings.value("empresa/logo").toString()

    def tabClose(self):

        # Remove o Tabulador caso o titulo nao seja "Bem Vindo"
        if self.tab.tabText(self.tab.currentIndex()) != "Bem Vindo" :self.tab.removeTab(self.tab.currentIndex())
        self.totalTabs = self.tab.count()

    def listaclientes(self):

        # verifies if in the list of tabs finds the name
        for item in range(0, self.tab.count()+1, 1):

            # if finds the selects the current tab and returns
            if self.tab.tabText(item) == "Lista de Clientes":
                self.tab.setCurrentIndex(item)
                return

        # Did not find then makes one
        import lista_de_clientes

        clientes = lista_de_clientes.MainWindow(self)

        self.fornecedores = self.tab.addTab(clientes, QIcon("./icons/clientes.ico"), "Lista de Clientes")
        clientes.show()
        self.tab.setCurrentIndex(self.fornecedores)

    def listafamilias(self):

        # verifies if in the list of tabs finds the name
        for item in range(0, self.tab.count()+1, 1):

            # if finds the selects the current tab and returns
            if self.tab.tabText(item) == "Lista de Famílias":
                self.tab.setCurrentIndex(item)
                return

        # Did not find then makes one
        import lista_de_familias

        familias = lista_de_familias.MainWindow(self)

        self.familias = self.tab.addTab(familias, QIcon("./icons/hotel.png"), "Lista de Famílias")
        familias.show()
        self.tab.setCurrentIndex(self.familias)
        
    def listasubfamilias(self):

        # verifies if in the list of tabs finds the name
        for item in range(0, self.tab.count()+1, 1):

            # if finds the selects the current tab and returns
            if self.tab.tabText(item) == "Lista de Sub Famílias":
                self.tab.setCurrentIndex(item)
                return

        # Did not find then makes one
        import lista_de_subfamilias

        subfamilias = lista_de_subfamilias.MainWindow(self)

        self.subfamilias = self.tab.addTab(subfamilias, QIcon("./icons/hotel.png"), "Lista de Sub Famílias")
        subfamilias.show()
        self.tab.setCurrentIndex(self.subfamilias)

    def listaprodutos(self):

        # verifies if in the list of tabs finds the name
        for item in range(0, self.tab.count() + 1, 1):

            # if finds the selects the current tab and returns
            if self.tab.tabText(item) == "Lista de Produtos/Serviços":
                self.tab.setCurrentIndex(item)
                return

        # Did not find then makes one
        import lista_de_produtos

        produtos = lista_de_produtos.MainWindow(self)

        self.produtos = self.tab.addTab(produtos, QIcon("./icons/hotel.png"), "Lista de Produtos/Serviços")
        produtos.show()
        self.tab.setCurrentIndex(self.produtos)

    def listaarmazems(self):

        # verifies if in the list of tabs finds the name
        for item in range(0, self.tab.count() + 1, 1):

            # if finds the selects the current tab and returns
            if self.tab.tabText(item) == "Lista de Armazéns":
                self.tab.setCurrentIndex(item)
                return

        # Did not find then makes one
        import lista_de_armazems

        armazems = lista_de_armazems.MainWindow(self)

        self.armazems = self.tab.addTab(armazems, QIcon("./icons/hotel.png"), "Lista de Armazéns")
        armazems.show()
        self.tab.setCurrentIndex(self.armazems)

    def listataxas(self):

        # verifies if in the list of tabs finds the name
        for item in range(0, self.tab.count() + 1, 1):

            # if finds the selects the current tab and returns
            if self.tab.tabText(item) == "Lista de Taxas":
                self.tab.setCurrentIndex(item)
                return

        # Did not find then makes one
        import lista_de_taxas

        taxas = lista_de_taxas.MainWindow(self)

        self.taxas = self.tab.addTab(taxas, QIcon("./icons/taxas.png"), "Lista de Taxas")
        taxas.show()
        self.tab.setCurrentIndex(self.taxas)

    def listastock(self):

        # verifies if in the list of tabs finds the name
        for item in range(0, self.tab.count() + 1, 1):

            # if finds the selects the current tab and returns
            if self.tab.tabText(item) == "Lista de Stock":
                self.tab.setCurrentIndex(item)
                return

        # Did not find then makes one
        import lista_de_stock

        stock = lista_de_stock.MainWindow(self)

        self.stock = self.tab.addTab(stock, QIcon("./icons/hotel.png"), "Lista de Stock")
        stock.show()
        self.tab.setCurrentIndex(self.stock)

    def listadocumentos(self):

        # verifies if in the list of tabs finds the name
        for item in range(0, self.tab.count() + 1, 1):

            # if finds the selects the current tab and returns
            if self.tab.tabText(item) == "Lista de Documentos":
                self.tab.setCurrentIndex(item)
                return

        # Did not find then makes one
        import lista_de_documentos

        documentos = lista_de_documentos.MainWindow()

        self.documentos = self.tab.addTab(documentos, QIcon("./icons/hotel.png"), "Lista de Documentos")
        documentos.show()
        self.tab.setCurrentIndex(self.documentos)

    def listausers(self):

        # verifies if in the list of tabs finds the name
        for item in range(0, self.tab.count() + 1, 1):

            # if finds the selects the current tab and returns
            if self.tab.tabText(item) == "Lista de Usuários":
                self.tab.setCurrentIndex(item)
                return

        # Did not find then makes one
        import lista_de_users

        users = lista_de_users.MainWindow(self)

        self.users = self.tab.addTab(users, QIcon("./icons/users.ico"), "Lista de Usuários")
        users.show()
        self.tab.setCurrentIndex(self.users)

    def listafornecedores(self):
        # verifies if in the list of tabs finds the name
        for item in range(0, self.tab.count() + 1, 1):

            # if finds the selects the current tab and returns
            if self.tab.tabText(item) == "Lista de Fornecedores":
                self.tab.setCurrentIndex(item)
                return

        # Did not find then makes one
        import lista_de_fornecedores

        fornecedores = lista_de_fornecedores.MainWindow(self)

        self.fornecedores = self.tab.addTab(fornecedores, QIcon("./icons/fornecedores.ico"), "Lista de Fornecedores")
        fornecedores.show()
        self.tab.setCurrentIndex(self.fornecedores)

    def closeEvent(self,event):
        if QMessageBox.question(self, qApp.tr("Pergunta"),
                                qApp.tr("Deseja fechar o Programa?"), QMessageBox.No|QMessageBox.Yes) == QMessageBox.No:
            event.ignore()
        else:
            qApp.quit()
            # self.gravarIniciais()
            # self.db.close()

    def dadosIniciais(self):
        settings = QSettings()
        size = settings.value("main\size").toSize()
        pos = settings.value("main\pos").toPoint()
        tema = settings.value("main\tema").toString()

        self.resize(size)
        self.move(pos)

        self.setStyle(QStyleFactory.create(tema))

    def gravarIniciais(self):
        settings = QSettings()
        settings.setValue("main\size",QSize(self.size()))
        settings.setValue("main\pos",QPoint(self.pos()))
        settings.setValue("main\tema",self.estilo)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Gestor()
    w.setWindowTitle('Microgest POS')
    sys.exit(app.exec_())
