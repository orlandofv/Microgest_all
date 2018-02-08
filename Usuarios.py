# -*- coding: latin-1 -*-
"""
Created on Fri Mar 02 23:18:43 2012

@author: lims
"""


import sys

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QFormLayout, QVBoxLayout, QToolBar, QMessageBox,\
    QTextEdit, QAction, QApplication, QGroupBox, QCalendarWidget, QComboBox, QDateEdit
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
import sqlite3 as lite
from utilities import SEXO, PAISES, TIPO_DOC
filename = "dados.tsdb"


class user(QDialog):
    
    def __init__(self,parent=None):
        super(user,self).__init__(parent)

        self.accoes()
        self.ui()

        self.db = self.connect_db()
        # self.cur = self.parent().cur
        # self.conn = self.parent().conn

    def ui(self):
        html = """<center style= "{color:blue;}" > <h2 > Cadastro de Usuários </h2> </center> """

        titulo = QLabel(html)
        
        u_id = QLabel("Usuário")
        senha = QLabel("Senha") 
        senha2 = QLabel("Confirme a Senha") 
        
        self.u_id = QLineEdit()
        self.u_id.setMaxLength(15)
        self.senha = QLineEdit()
        self.senha.setEchoMode(QLineEdit.Password)
        self.senha.setMaxLength(15)
        self.senha2 = QLineEdit()
        self.senha2.setEchoMode(QLineEdit.Password)
        self.senha2.setMaxLength(15)
        
        lay1 = QFormLayout()
        lay1.addRow(u_id,self.u_id)
        lay1.addRow(senha,self.senha)
        lay1.addRow(senha2,self.senha2)
        
        grupo1 = QGroupBox("Dados de Entrada no sistema")
        grupo1.setLayout(lay1)

        cod = QLabel("Codigo")
        nome = QLabel("Primeiros nomes")
        endereco = QLabel("Endereço")
        sexo = QLabel("Sexo")
        email = QLabel("Email")
        nascimento = QLabel("Data de nascimento")
        contacto = QLabel("Contactos")
        tipo = QLabel("Tipo de Identificação")
        numero = QLabel("Número do documento")
        nacionalidade = QLabel("País")
        obs = QLabel("Observações")
        
        calendario = QCalendarWidget()
        calendario1 = QCalendarWidget()
        
        self.cod = QLineEdit()
        self.cod.setMaximumWidth(140)
        self.cod.setObjectName("cod")
        self.cod.setAlignment(Qt.AlignRight)
        self.cod.setEnabled(False)
        self.nome =  QLineEdit()
        self.apelido = QLineEdit()
        self.endereco = QLineEdit()
        self.sexo = QComboBox()
        self.sexo.setMaximumWidth(140)
        self.sexo.addItems(SEXO)
        self.email = QLineEdit()
        self.nascimento = QDateEdit()
        self.nascimento.setObjectName("cal1")
        self.nascimento.setCalendarPopup(True)
        self.nascimento.setCalendarWidget(calendario)
        self.nascimento.setMaximumWidth(140)
        self.nascimento.setAlignment(Qt.AlignRight)
        self.contacto =  QLineEdit()
        self.emergencia = QLineEdit()
        self.tipo =  QComboBox()
        self.tipo.setMaximumWidth(140)
        self.tipo.addItems(TIPO_DOC)
        self.numero =QLineEdit()
        self.numero.setMaximumWidth(140)
        self.numero.setMaxLength(15)
        self.numero.setAlignment(Qt.AlignRight)
        self.nacionalidade =QComboBox()
        self.nacionalidade.setMaximumWidth(280)
        self.nacionalidade.addItems(PAISES)
        self.validade  = QDateEdit()
        self.validade.setCalendarPopup(True)
        self.validade.setCalendarWidget(calendario1)
        self.validade.setObjectName("cal2")
        self.validade.setMaximumWidth(140)
        self.validade.setAlignment(Qt.AlignRight)
        self.obs =QTextEdit()

        grid = QFormLayout()

        grid.addRow(nome          ,self.nome             )
        # grid.addRow(apelido       ,self.apelido          )
        grid.addRow(endereco      ,self.endereco         )
        grid.addRow(sexo          ,self.sexo             )
        grid.addRow(email         ,self.email            )
        grid.addRow(nascimento    ,self.nascimento       )
        grid.addRow(contacto      ,self.contacto         )
        # grid.addRow(emergencia    ,self.emergencia       )
        grid.addRow(tipo          ,self.tipo             )
        grid.addRow(numero        ,self.numero           )
        grid.addRow(nacionalidade ,self.nacionalidade    )
        # grid.addRow(validade      ,self.validade         )
        grid.addRow(obs           ,self.obs              )

        grupo2 = QGroupBox("Dados Pessoais")
        grupo2.setLayout(grid)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(titulo)
        mainLayout.addWidget(grupo1)
        mainLayout.addWidget(grupo2)
        mainLayout.addWidget(self.tool)
        self.setLayout(mainLayout)

        self.setWindowTitle("Cadastro de usuarios")
        
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

    def accoes(self):
        self.tool = QToolBar()
        
        gravar = QAction(QIcon("./icons/SaveGreen.ico"),"&Gravar dados",self)
        eliminar = QAction(QIcon("./icons/Delete.ico"),"&Eliminar dados",self)
        fechar = QAction(QIcon("./icons/filequit.png"),"&Fechar",self)

        self.tool.addAction(gravar)
        self.tool.addAction(eliminar)
      
        self.tool.addSeparator()
        self.tool.addAction(fechar)

        gravar.triggered.connect(self.addRecord)
        eliminar.triggered.connect(self.limpar)
        fechar.triggered.connect(self.fechar)

        self.setTabletTracking(True)

    def closeEvent(self, evt):
        parent = self.parent()
        if parent is not None:
            parent.fill_table()

    def fechar(self):
        self.close()
    
    def limpar(self):
        for child in self.findChildren(QLineEdit) or child in self.findChildren(QTextEdit) :
            if child.objectName() not in ["cod","cal1","cal2"]:
                child.clear()
                self.u_id.setFocus()
                
    def connect_db(self):
        # Connect to database and retrieves data
        try:
            self.conn = lite.connect(filename)
            self.cur = self.conn.cursor()

        except lite.Error as e:
            QMessageBox.critical(self, "Erro ao conectar a Base de Dados",
                                 "Os seus Dados não foram gravados. Erro: {erro} ".format(erro=e))
            sys.exit(True)
    
    def validacao(self):

        if self.u_id.text() == "":
            QMessageBox.information(self, "Erro", "Nome do usuário inválido")
            self.u_id.setFocus()
            return False
        elif len(self.u_id.text()) < 2:
            QMessageBox.information(self, "Erro", "Nome do usuário deve ter no mínimo 2 Caracteres")
            self.u_id.setFocus()
            return False
        elif len(self.senha.text()) < 6:
            QMessageBox.information(self, "Erro", "Senha deve ter no mínimo 6 Caracteres")
            self.senha.setFocus()
            return False
        elif self.senha2.text() != self.senha.text():
            QMessageBox.information(self, "Erro", "Senha de confirmação diferente")
            self.senha2.setFocus()
            return False
        else:
            return True

    def mostrarReg(self):
        sql = """select * from users where cod = "{codigo}" """.format(codigo=self.u_id.text())

        self.cur.execute(sql)
        dados =  self.cur.fetchall()

        for item in dados:

            self.senha.setText(item[1])
            self.senha2.setText(item[2])
            self.nome.setText(item[3])
            self.endereco.setText(item[4])
            self.sexo.setCurrentText(item[5])
            self.email.setText(item[6])
            self.nascimento.setDate(QDate.fromString(item[7]))
            self.contacto.setText(item[8])
            self.tipo.setCurrentText(item[9])
            self.numero.setText(item[10])
            self.nacionalidade.setCurrentText(item[11])
            self.obs.setPlainText(item[12])

    def addRecord(self):

        if self.validacao() is True:
            cod = self.u_id.text()
            senha = self.senha.text()
            senha2 = self.senha2.text()
            nome = self.nome.text()
            endereco = self.endereco.text()
            sexo = self.sexo.currentText()
            email = self.email.text()
            nascimento = QDate(self.nascimento.date()).toString()
            contacto = self.contacto.text()
            tipo = self.tipo.currentText()
            numero = self.numero.text()
            nacionalidade = self.nacionalidade.currentText()
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

            estado = 1

            if self.existe(cod) == True:
                sql = """UPDATE users set senha="{senha}", senha2="{senha2}", nome="{nome}", endereco="{endereco}",
                 sexo="{sexo}", email="{email}", nascimento="{nascimento}", contacto="{contacto}", tipo="{tipo}", 
                 numero="{numero}", nacionalidade="{nacionalidade}", obs="{obs}", created="{created}", 
                 modified="{modified}", modified_by="{modified_by}", created_by="{created_by}",
                 estado="{estado}" where cod="{cod}" """.format(cod=cod,senha=senha, senha2=senha2, nome=nome,
                                                                endereco=endereco,
                                             sexo=sexo, email=email, nascimento=nascimento, contacto=contacto,
                                             tipo=tipo, numero=numero, nacionalidade=nacionalidade, obs=obs,
                                             created=created, modified=modified, modified_by=modified_by,
                                             created_by=created_by, estado=estado)
            else:
                values = """ "{cod}", "{senha}", "{senha2}", "{nome}", "{endereco}", "{sexo}", "{email}",
                 "{nascimento}", "{contacto}", "{tipo}", "{numero}", "{nacionalidade}", "{obs}", "{created}", 
                 "{modified}", "{modified_by}", "{created_by}",
                  "{estado}" """.format(cod=cod, senha=senha, senha2=senha2, nome=nome, endereco=endereco,
                                             sexo=sexo, email=email, nascimento=nascimento, contacto=contacto,
                                             tipo=tipo, numero=numero, nacionalidade=nacionalidade, obs=obs,
                                             created=created, modified=modified, modified_by=modified_by,
                                             created_by=created_by, estado=estado)

                sql = """INSERT INTO users (cod, senha, senha2, nome, endereco, sexo, email, nascimento, contacto, tipo,
                 numero, nacionalidade, obs, created, modified, modified_by, created_by, 
                 estado) VALUES ({values})""".format(values=values)

            try:
                self.cur.execute(sql)
                self.conn.commit()
                # messagem = QMessageBox.information(self,"Informação","Registro Gravado com sucesso!",QMessageBox.Ok)
                
                if QMessageBox.question(self,"Pergunta","Registo Gravado com sucesso!\nDeseja Cadastrar outro Item?",
                               QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
                    self.limpar()
                else:
                    self.close()

            except lite.Error as e:
                erro =  "Erro: %s . Reporte ao suporte." % e
                QMessageBox.critical(self,"Erro","Dados não gravados." + erro ,QMessageBox.Ok)
                return

    def existe(self, codigo):

        sql = """SELECT cod from users where cod = "{codigo}" """.format(codigo=str(self.u_id.text()))

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

    def closeEvent(self,evt):

        parente =  self.parent()

        if parente is None:
            return

        parente.fill_table()

# app =QApplication(sys.argv)
# main_form = user()
# main_form.show()
# app.exec_()


    
      
