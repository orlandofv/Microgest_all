#-*- coding:latin-1 -*-

from PyQt5.QtSql import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
ACTIVAS = []

class produtos(QMainWindow):
    
    def __init__(self, parent=None):
        super(produtos,self).__init__(parent)
        
        self.gravar = True
        
    def gui(self):
        
        tab = QTabWidget()
        
        cod = QLabel("C�digo")
        designacao = QLabel("Designa��o")
        designacao_diminuida = QLabel("Curta Designa��o")
        descricaoo = QLabel("Descri��o(255 m�x.)")
        cod_de_barras = QLabel("C�digo de Barras")
        
        fabricante = QLabel("Fabricante")        
        referencia = QLabel("Refer�ncia")
        fornecedor = QLabel("Fornecedor")
        
        quantidade = QLabel("Quantidade")
        quantidade_minima = QLabel("Quantidade M�nima")
        
        custo = QLabel("Custo")
        
        venda_retalho = QLabel("Venda a Retalho")
        venda_grosso = QLabel("Venda a Grosso")
        promocao = QLabel("Pre�o de Promo��o")
        abate = QLabel("Pre�o de Abate")
        saldo = QLabel("Pre�o de Saldos")
        
        validade = QLabel("Data de Validade")
        
        fotografia = QLabel("Imagem")
        
        
        
        
        
