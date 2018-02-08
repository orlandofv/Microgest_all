# -*- coding: latin-1 -*-
"""
Created on Fri Mar 02 23:18:43 2012

@author: lims
"""
import sys

from PyQt5.QtSql import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QTextEdit, QPushButton, QFormLayout, QVBoxLayout, QFileDialog,\
    QToolBar, QAction, QMessageBox, QApplication
import sqlite3 as lite

filename = "dados.tsdb"


class Empresa(QDialog):

    def __init__(self, parent=None):
        super(Empresa, self).__init__(parent)

        self.resize(600,600)
        # self.logtipo = ""
        # self.connect_db()
        # self.accoes()
        # self.ui()

    def connect_db(self):
        # Connect to database and retrieves data
        try:
            self.conn = lite.connect(filename)
            self.cur = self.conn.cursor()

        except lite.Error as e:
            QMessageBox.critical(self, "Erro ao conectar a Base de Dados",
                                 "Os seus Dados não foram gravados. Erro: {erro} ".format(erro=e))
            sys.exit(True)

    def ui(self):
        html = """<center style= "{color:red;}" > <h2 > Cadastro de empresas </h2> </center> """
        validator2 = QRegExp("^[a-zA-Z ]{1,50}$")
      
        titulo = QLabel(html)
        nome = QLabel("Nome da Empresa")
        cabecalho = QLabel("Cabeçalho")

        self.nome = QLineEdit()
        self.cabecalho = QTextEdit()
        self.btn = QPushButton("Logo")

        logoHtml = """ QLabel{
            width:40px;
             border-color: #9B9B9B;
             border-bottom-color: #C2C7CB; /* same as pane color */
         }"""

        self.logo = QLabel("Logo")
        self.logo.setStyleSheet(logoHtml)

        self.btn.clicked.connect(self.escolhaLogo)

        grid = QFormLayout()
        grid.addRow(nome,self.nome)
        grid.addRow(cabecalho,self.cabecalho)
        grid.addRow(self.btn,self.logo)

        vLay = QVBoxLayout(self)
        vLay.setContentsMargins(0,0,0,0)
        
        cLay = QVBoxLayout()
        cLay.setContentsMargins(10,10,10,10)
        cLay.addLayout(grid)
        
        vLay.addWidget(titulo)
        vLay.addLayout(cLay)
        vLay.addWidget(self.tool)

        self.setWindowTitle("Dados da Empresa")
        
        style = """
            margin: 0;
            padding: 0;
            border-image:url(./icons/transferir.jpg) 30 30 stretch;
            background:#303030;
            font-family: Arial, Helvetica, sans-serif;
            font-size: 12px;
            color: #FFFFFF;
        
        """ 
        
        titulo.setStyleSheet(style)
        
        style2 = """
            QDialog{margin: 0;
        	padding: 0;
            border-image:url(./icons/aqua.JPG) 30 30 stretch;
            background:#C0C0CC;
        	font-family: Arial, Helvetica, sans-serif;
        	font-size: 12px;
        	color: #FFFFFF;}
        """ 
        
        self.setStyleSheet(style2)

    def escolhaLogo(self):
        self.path = "./icons"
        formats = "*.bmp *.jpg *.png *.ico"
        path = QFileDialog.getOpenFileName(self,"Escolha a Foto", self.path,formats)

        if path.isEmpty():
            caminho = "./icons/3d chart.ico"
        else:
            caminho = path

        self.logo.setPixmap(QPixmap.fromImage(QImage("caminho".format(caminho=caminho))))
        self.logtipo = caminho

    def accoes(self):
        self.tool = QToolBar()
        
        gravar = QAction(QIcon("./icons/SaveGreen.ico"),"&Gravar dados",self)
        eliminar = QAction(QIcon("./icons/Delete.ico"),"&Eliminar dados",self)

        fechar = QAction(QIcon("./icons/filequit.png"),"&Fechar",self)
        
        self.tool.addAction(gravar)
        self.tool.addAction(eliminar)
        self.tool.addSeparator()
        self.tool.addAction(fechar)

# ==============================================================================
        gravar.triggered.connect(self.gravar)
        eliminar.triggered.connect(self.apagar)
        fechar.triggered.connect(self.fechar)
# ==============================================================================
        
    def fechar(self):
        self.close()
    
    def mostrarReg(self):
        setings = QSettings()
        nome = setings.value("empresa/nome").toString()
        cabecalho = setings.value("empresa/cabecalho").toString()
        logo = setings.value("empresa/logo").toString()

        self.nome.setText(nome)
        self.cabecalho.setHtml(cabecalho)
        self.logo.setPixmap(QPixmap.fromImage(QImage("logo".format(logo=logo))))

    def showEvent(self, evt):
        self.mostrarReg()
    
    def validacao(self):
        setings = QSettings()
        nome = setings.value("empresa/nome").toString()
        cabecalho = setings.value("empresa/cabecalho").toString()
        logo = setings.value("empresa/logo")

        self.nome.setText(nome)
        self.cabecalho.setHtml(cabecalho)
        self.logo.setText(logo)

    def apagar(self):
        self.nome.clear()
        self.cabecalho.clear()

    def gravar(self):

        nome = str(self.nome.text())
        cabecalho = str(self.cabecalho.toHtml())
        logo = self.logtipo

        setings = QSettings()
        setings.setValue("empresa/nome",nome)
        setings.setValue("empresa/cabecalho",cabecalho)
        setings.setValue("empresa/logo",logo)
        QMessageBox.information(self,"Sucesso","Registo gravado com sucesso")

    def closeEvent(self,evt):
        parente =  self.parent()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    helloPythonWidget = Empresa()
    helloPythonWidget.show()
    sys.exit(app.exec_())
