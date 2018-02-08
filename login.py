# -*- coding: latin-1 -*-

from PyQt5.QtSql import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QComboBox, QWidget, QVBoxLayout, \
    QGridLayout, QApplication, QMessageBox
import math
import sys
import sqlite3 as lite

import main

filename = "dados.tsdb"

class Login(QDialog):


    def __init__(self,parent=None):
        super(Login,self).__init__(parent)

        self.tentativas = 5
        self.contador = 0

        titulo = QLabel( """<center style="color:blue;
        border: 10px 10px 10px 10px" > <h1> Dados de Entrada </h1> </center> """)
        self.connect_db()

        self.users = QComboBox()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        # self.password.setMinimumHeight(50)
        # self.password.setFocusPolicy(Qt.NoFocus)
        self.ok = QPushButton("&OK")
        self.ok.setDefault(True)
        self.fechar = QPushButton("&Fechar")

        self.ok.setIcon(QIcon("./icons/close_2.ico"))

        self.password.setMaxLength(30)

        vlay = QVBoxLayout()

        self.limpar = QPushButton("&Limpar")
        self.btnCalc0 = QPushButton("0",self)
        self.btnCalc1 = QPushButton("1",self)
        self.btnCalc2 = QPushButton("2",self)
        self.btnCalc3 = QPushButton("3",self)
        self.btnCalc4 = QPushButton("4",self)
        self.btnCalc5 = QPushButton("5",self)
        self.btnCalc6 = QPushButton("6",self)
        self.btnCalc7 = QPushButton("7",self)
        self.btnCalc8 = QPushButton("8",self)
        self.btnCalc9 = QPushButton("9",self)

        btn_grid = QGridLayout()

        btn_grid.addWidget(self.users, 0, 0, 1, 3)
        btn_grid.addWidget(self.password, 1, 0, 1, 3)
        btn_grid.addWidget(self.btnCalc7, 2, 0)
        btn_grid.addWidget(self.btnCalc8, 2, 1)
        btn_grid.addWidget(self.btnCalc9, 2, 2)
        btn_grid.addWidget(self.btnCalc4, 3, 0)
        btn_grid.addWidget(self.btnCalc5, 3, 1)
        btn_grid.addWidget(self.btnCalc6, 3, 2)
        btn_grid.addWidget(self.btnCalc1, 4, 0)
        btn_grid.addWidget(self.btnCalc2, 4, 1)
        btn_grid.addWidget(self.btnCalc3, 4, 2)
        btn_grid.addWidget(self.btnCalc0, 5, 0)
        btn_grid.addWidget(self.limpar, 5, 1)
        btn_grid.addWidget(self.fechar, 5, 2)
        btn_grid.addWidget(self.ok, 6, 0, 1, 3)

        self.setLayout(btn_grid)

        style = """
        QDialog{border-image: url(icons/AquaLoop.jpg);} 
        
         QPushButton , QWidget#self.center{
             background: #0C9 ;
             border-style: outset;
             border-width: 2px;
             border-radius: 10px;
             border-color: beige;
             font: bold 24px;
             min-width: 5em;
             min-height: 50px;
             padding: 6px;
         }
         
          QLineEdit {
             background-color:#9FF ;
             border-style: outset;
             border-width: 2px;
             border-radius: 10px;
             border-color: beige;
             font: bold 24px;
             min-width: 5em;
             min-height: 50px;
             padding: 6px;
         }
         
        QPushButton:hover {
             background-color: red;
         }
         
        QPushButton:pressed {
             background-color: #141414;
             color:white;
         }
        """

        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setStyleSheet(style)
        # self.setWindowState(Qt.WindowMaximized)
        # self.showFullScreen()

        self.setWindowTitle("Dados de Entrada")
        self.setWindowIcon(QIcon("./icons/Deleket-Sleek-Xp-Basic-Administrator.ico"))

        self.ok.clicked.connect(self.aceite)
        self.fechar.clicked.connect(sys.exit)

        self.btnCalc0.clicked.connect(self.key0)
        self.btnCalc1.clicked.connect(self.key1)
        self.btnCalc2.clicked.connect(self.key2)
        self.btnCalc3.clicked.connect(self.key3)
        self.btnCalc4.clicked.connect(self.key4)
        self.btnCalc5.clicked.connect(self.key5)
        self.btnCalc6.clicked.connect(self.key6)
        self.btnCalc7.clicked.connect(self.key7)
        self.btnCalc8.clicked.connect(self.key8)
        self.btnCalc9.clicked.connect(self.key9)
        self.limpar.clicked.connect(self.Limpar)

        # self.resize(300, 300)
        self.setMinimumSize(300, 320)
        self.setMaximumSize(300, 320)
        self.encheusers()
        
    def connect_db(self):
        # Connect to database and retrieves data
        try:
            self.conn = lite.connect(filename)
            self.cur = self.conn.cursor()

        except lite.Error as e:
            QMessageBox.critical(self, "Erro ao conectar a Base de Dados",
                                 "Os seus Dados não foram gravados. Erro: {erro} ".format(erro=e))
            sys.exit(True)

    def aceite(self):
        sql = """select cod, senha from users where cod="{cod}" and senha="{senha}"
         """.format(cod=self.users.currentText(), senha=self.password.text())

        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
        except lite.Error as e:
            return

        if len(data) == 0:

            self.contador += 1

            tentativas = 5 - self.contador

            if tentativas == 0:
                sys.exit()

            QMessageBox.information(self, "Credências Errados", "Por Favor verifique seus dados!!! \n "
                                                             "Faltam {contador} Tentativas".format(contador=tentativas))
            self.Limpar()
            return
        else:
            self.parent().user = data[0][0]
            self.parent().accoes()
            self.parent().showMaximized()
            self.hide()

    def encheusers(self):
        sql = "SELECT cod FROM users"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        
        if len(data) > 0:
            for item in data:
                self.users.addItems(item)

    def Limpar(self):
        self.password.setText("")
        
    def key0(self):
        self.password.setFocus()
        self.password.setText(self.password.text() + self.btnCalc0.text())
        self.password.clearFocus()
    
    def key1(self):
        self.password.setFocus()
        self.password.setText(self.password.text() + self.btnCalc1.text())
        self.password.clearFocus()
    
    def key2(self):
        self.password.setFocus()
        self.password.setText(self.password.text() + self.btnCalc2.text())
        self.password.clearFocus()
    
    def key3(self):
        self.password.setFocus()
        self.password.setText(self.password.text() + self.btnCalc3.text())
        self.password.clearFocus()
    
    def key4(self):
        self.password.setFocus()
        self.password.setText(self.password.text() + self.btnCalc4.text())
        self.password.clearFocus()
    
    def key5(self):
        self.password.setFocus()
        self.password.setText(self.password.text() + self.btnCalc5.text())
        self.password.clearFocus()
    
    def key6(self):
        self.password.setFocus()
        self.password.setText(self.password.text() + self.btnCalc6.text())
        self.password.clearFocus()
    
    def key7(self):
        self.password.setFocus()
        self.password.setText(self.password.text() + self.btnCalc7.text())
        self.password.clearFocus()
    
    def key8(self):
        self.password.setFocus()
        self.password.setText(self.password.text() + self.btnCalc8.text())
        self.password.clearFocus()
    
    def key9(self):
        self.password.setFocus()
        self.password.setText(self.password.text() + self.btnCalc9.text())
        self.password.clearFocus()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def showEvent(self, evt):
        self.center()

    def closeEvent(self, evt):
        sys.exit


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     helloPythonWidget = Login()
#     helloPythonWidget.show()
#     sys.exit(app.exec_())