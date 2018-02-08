# -*- coding: latin-1 -*-
"""
Created on Tue Oct 01 18:52:29 2013

@author: itbl_orlando
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QLabel, QFrame, QHBoxLayout, QVBoxLayout
import os

class startPage(QDialog):
    def __init__(self,parent=None):
        super(startPage,self).__init__(parent)
        
        #diocionácio do sistema operativo
        dic = os.environ
        
        cp = dic['COMPUTERNAME']
        pu = dic['USERNAME']
        pc = QLabel("Terminal: %s " % cp, self)
        pc_user = QLabel("Licenciado para: %s " % pu, self)
        usuario = QLabel("Usuário: %s " % self.parent().user, self)
        
        bmvindo = QLabel("Bem Vindo, %s." % self.parent().user , self)
        bmvindo.setAlignment(Qt.AlignCenter)
        font = QFont("Courier New", 24)
        bmvindo.setFont(font)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
    
        lay = QVBoxLayout()
        
        lay.addStretch()
        lay.addWidget(bmvindo,Qt.AlignCenter)
        lay.addStretch()
        lay.addWidget(pc)
        lay.addWidget(pc_user)
        lay.addWidget(line)
        lay.addWidget(usuario)
        
        self.setLayout(lay)
        
        style2 ="""
        QDialog{
        	border-image: url(./icons/luxury_hotel-wallpaper-1680x1260.jpg);
            }
            """

        self.setStyleSheet(style2)
        
#if __name__ == "__main__":
#    app = QApplication(sys.argv)
#    wnd = startPage()
#    wnd.show()
#    sys.exit(app.exec_())