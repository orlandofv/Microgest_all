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
        
        cod = QLabel("Código")
        designacao = QLabel("Designação")
        designacao_diminuida = QLabel("Curta Designação")
        descricaoo = QLabel("Descrição(255 máx.)")
        cod_de_barras = QLabel("Código de Barras")
        
        fabricante = QLabel("Fabricante")        
        referencia = QLabel("Referência")
        fornecedor = QLabel("Fornecedor")
        
        quantidade = QLabel("Quantidade")
        quantidade_minima = QLabel("Quantidade Mínima")
        
        custo = QLabel("Custo")
        
        venda_retalho = QLabel("Venda a Retalho")
        venda_grosso = QLabel("Venda a Grosso")
        promocao = QLabel("Preço de Promoção")
        abate = QLabel("Preço de Abate")
        saldo = QLabel("Preço de Saldos")
        
        validade = QLabel("Data de Validade")
        
        fotografia = QLabel("Imagem")
        
        
        
        
        
