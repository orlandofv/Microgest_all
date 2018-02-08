# -*- coding: latin-1 -*-
"""
Created on Fri Mar 02 23:18:43 2012

@author: lims
"""

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QDoubleSpinBox, QFormLayout, QVBoxLayout, QToolBar, QMessageBox, \
    QTextEdit, QAction, QApplication
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
import sys

from utilities import codigo as cd
from database import DBCOnnection

import sqlite3 as lite

filename = "dados.tsdb"


class fornecedor(QDialog):
    def __init__(self, parent=None):
        super(fornecedor, self).__init__(parent)

        self.accoes()
        self.ui()

        self.db = self.connect_db()
        # self.cur = self.parent().cur
        # self.conn = self.parent().conn

        # verifica a existencia dos dados na base de dados
        self.existe(self.cod.text())

        # Mostraregisto caso exista
        self.mostrarReg()

    def ui(self):
        html = """<center style= "{color:blue;}" > <h2 > Cadastro de fornecedor </h2> </center> """

        titulo = QLabel(html)
        cod = QLabel("Codigo")
        nome = QLabel("Nome")
        endereco = QLabel("Endere�o")
        nuit = QLabel("NUIT")
        email = QLabel("Email")
        contacto = QLabel("Contactos")
        desconto = QLabel("Desconto nas Compras (%)")
        obs = QLabel("Observa��es")

        self.cod = QLineEdit()
        self.cod.setMaximumWidth(140)
        self.cod.setObjectName("cod")
        self.cod.setAlignment(Qt.AlignRight)
        self.cod.setDisabled(True)
        self.nome = QLineEdit()
        self.nome.setMaxLength(50)
        self.endereco = QLineEdit()
        self.NUIT = QLineEdit()
        self.NUIT.setAlignment(Qt.AlignRight)
        self.NUIT.setMaxLength(9)
        self.email = QLineEdit()
        self.email.setMaxLength(50)
        self.contacto = QLineEdit()
        self.contacto.setMaxLength(255)
        self.desconto = QDoubleSpinBox()
        self.setMaximumHeight(100)
        self.obs = QTextEdit()
        grid = QFormLayout()

        grid.addRow(cod, self.cod)
        grid.addRow(nome, self.nome)
        grid.addRow(endereco, self.endereco)
        grid.addRow(nuit, self.NUIT)
        grid.addRow(email, self.email)
        grid.addRow(contacto, self.contacto)
        # grid.addRow(desconto, self.desconto)
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

        self.setWindowTitle("Cadastro de fornecedores")

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

        # gera novo codigo para fornecedores
        from utilities import codigo
        self.cod.setText("FR" + codigo("FR" + "ABCDEF1234567890"))

    def validacao(self):

        if str(self.nome.text()) == "":
            QMessageBox.information(self, "Erro", "Nome do fornecedor inv�lido")
            self.nome.setFocus()
            return False
        else:
            return True

    def mostrarReg(self):

        sql = """SELECT * from fornecedores where cod = "{codigo}" """.format(codigo=str(self.cod.text()))
        self.cur.execute(sql)
        data = self.cur.fetchall()

        if len(data) == 0:
            self.cod.setText("FR" + cd("ABCDEF1234567890"))
        else:
            self.nome.setText(''.join(data[0][1]))
            self.endereco.setText(''.join(data[0][2]))
            self.NUIT.setText(''.join(data[0][3]))
            self.email.setText(''.join(data[0][4]))
            self.contacto.setText(''.join(data[0][5]))
            self.obs.setPlainText(''.join(data[0][6]))

    def existe(self, codigo):

        sql = """SELECT cod from fornecedores where cod = "{codigo}" """.format(codigo=str(self.cod.text()))

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
            endereco = self.endereco.text()
            nuit = self.NUIT.text()
            email = self.email.text()
            contactos = self.contacto.text()
            obs = self.obs.toPlainText()
            estado = 1
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


                sql = """UPDATE fornecedores set nome="{nome}", endereco="{endereco}", NUIT="{NUIT}", email="{email}", 
                contactos="{contactos}", obs="{obs}", modified="{modified}", 
                modified_by="{modified_by}" where cod="{cod}" """.format(cod=code, nome=nome, endereco=endereco,
                                                                         NUIT=nuit, email=email, contactos=contactos,
                                                                         obs=obs,
                                                                         modified=modified, modified_by=modified_by)
                try:
                    self.cur.execute(sql)
                    self.conn.commit()
                except lite.Error as e:
                    QMessageBox.critical(self, "Erro", "Os seus Dados n�o foram gravados. Erro: {erro} ".format(erro=e))
                    return
            else:

                values = """ "{cod}", "{nome}", "{endereco}", "{NUIT}", "{email}", "{contactos}", "{obs}",
                         "{estado}", "{created}", "{modified}", "{modified_by}", "{created_by}" """.format(cod=code,
                                                                                                           nome=nome,
                                                                                                           endereco=endereco,
                                                                                                           NUIT=nuit,
                                                                                                           email=email,
                                                                                                           contactos=contactos,
                                                                                                           obs=obs,
                                                                                                           estado=estado,
                                                                                                           created=created,
                                                                                                           modified=modified,
                                                                                                           modified_by=modified_by,
                                                                                                           created_by=created_by)
                try:
                    sql = "INSERT INTO fornecedores (cod, nome, endereco, NUIT,email, contactos, obs, estado, created, " \
                          "modified, modified_by, created_by) values({value})".format(value=values)

                    self.cur.execute(sql)
                    self.conn.commit()
                except lite.Error as e:
                    QMessageBox.critical(self, "Erro", "Os seus Dados n�o foram gravados. Erro: {erro} ".format(erro=e))
                    return

            if QMessageBox.question(self, "Pergunta", "Registo Gravado com sucesso!\nDeseja Cadastrar outro Item?",
                                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                if self.parent() is not None: self.parent().actualizar = False
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
                                 "Os seus Dados n�o foram gravados. Erro: {erro} ".format(erro=e))
            sys.exit(True)

#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     helloPythonWidget = fornecedor()
#     helloPythonWidget.show()
#
#     sys.exit(app.exec_())