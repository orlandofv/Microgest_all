import sys
import operator

from PyQt5.QtWidgets import QApplication, QTableView, QAbstractItemView, QMessageBox, QToolBar, \
    QLineEdit, QLabel, QStatusBar, QAction, QMainWindow, qApp

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex
import sqlite3 as lite
# from base import filename, DBCOnnection
from functools import partial
from familia import Cliente

filename = 'dados.tsdb'


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # controla o codigo
        self.current_id = ""

        # Connect the Database
        if self.parent() is None:
            self.db = self.connect_db()
            self.user = ""
        else:
            self.conn = self.parent().conn
            self.cur = self.parent().cur
            self.user = self.parent().user

        # Create the main user interface
        self.ui()

        # Header for the table
        self.header = [qApp.tr('Código'), qApp.tr('Descrição'), qApp.tr('Observações')]

        # Search the data
        self.fill_table()
        self.find_w.textEdited.connect(self.fill_table)

    def ui(self):

        # create the view
        self.tv = QTableView(self)

        # set the minimum size
        self.tv.setMinimumSize(400, 300)

        # hide grid
        self.tv.setShowGrid(False)

        self.tv.setSelectionBehavior(QAbstractItemView.SelectRows)
        # set the font

        # hide vertical header
        vh = self.tv.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties and stretch last column
        hh = self.tv.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        self.tv.resizeColumnsToContents()

        # enable sorting
        self.tv.setSortingEnabled(True)

        self.tv.clicked.connect(self.clickedSlot)
        self.tv.setAlternatingRowColors(True)
        self.tv.setFocus()
        self.setCentralWidget(self.tv)
        self.create_toolbar()

    def focusInEvent(self, evt):
        self.fill_table()

    def connect_db(self):
        # Connect to database and retrieves data
        try:
            self.conn = lite.connect(filename)
            self.cur = self.conn.cursor()

        except lite.Error as e:
            sys.exit(True)

    def fill_table(self):

        self.sql = """select cod, nome, obs from familia where nome like "%{nome}%" """.format(nome=self.find_w.text())

        try:
            self.cur.execute(self.sql)
            data = self.cur.fetchall()
        except lite.Error as e:
            return

        self.tabledata = data

        if len(data) == 0:
            return

        try:
            self.tm = MyTableModel(self.tabledata, self.header, self)
            # set the table model
            self.totalItems = self.tm.rowCount(self)
            self.tv.setModel(self.tm)
        except Exception as e:
            return
        # # set row height
        nrows = len(self.tabledata)
        for row in range(nrows):
            self.tv.setRowHeight(row, 25)
        self.create_statusbar()

    def create_toolbar(self):
        find = QLabel(qApp.tr("Search") + "  ")
        self.find_w = QLineEdit(self)
        self.find_w.setMaximumWidth(200)

        self.new = QAction(QIcon('./images/add.png'), qApp.tr("new"), self)
        self.delete = QAction(QIcon('./images/editdelete.png'), qApp.tr("delete"), self)
        self.print = QAction(QIcon('./images/fileprint.png'), qApp.tr("print"), self)
        self.update = QAction(QIcon('./images/pencil.png'), qApp.tr("update data"), self)

        tool = QToolBar()

        tool.addWidget(find)
        tool.addWidget(self.find_w)
        tool.addSeparator()
        tool.addAction(self.new)
        tool.addAction(self.update)
        tool.addSeparator()
        tool.addAction(self.delete)
        tool.addSeparator()
        tool.addAction(self.print)

        tool.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
        self.addToolBarBreak(Qt.BottomToolBarArea)
        self.addToolBar(tool)

        ######################################################################
        self.new.triggered.connect(self.new_data)
        self.delete.triggered.connect(self.removerow)
        self.tv.doubleClicked.connect(self.update_data)
        self.update.triggered.connect(self.update_data)
        # self.connect(self.delete, SIGNAL("triggered()"), self.removerow)
        # # self.connect(self.update, SIGNAL("triggered()"), self.updatedata)
        # self.print.triggered.connect(self.printForm)

    def create_statusbar(self):
        estado = QStatusBar(self)

        self.items = QLabel("Total Items: %s" % self.totalItems)
        estado.addWidget(self.items)
        self.setStatusBar(estado)

    def clickedSlot(self, index):

        self.row = int(index.row())

        indice = self.tm.index(self.row, 0)
        self.current_id = indice.data()

    def new_data(self):

        cl = Cliente(self)
        cl.setModal(True)
        cl.show()

    def update_data(self):

        if self.current_id == "":
            QMessageBox.information(self, "Info", "Seleccione o registo a actualizar na tabela")
            return

        cl = Cliente(self)
        cl.cod.setText(self.current_id)
        cl.mostrarReg()
        cl.setModal(True)
        cl.show()

    def removerow(self):

        if self.current_id == "":
            QMessageBox.information(self, "Info", "Seleccione o registo a apagar na tabela")
            return

        if QMessageBox.question(self, "Pergunta", str("Deseja eliminar o registo %s?") % self.current_id,
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            sql = """delete from familia where cod = "{codigo}" """.format(codigo=str(self.current_id))

            try:
                self.cur.execute(sql)
                self.conn.commit()
            except lite.Error as e:
                QMessageBox.warning(self, "Impossivel apagar dados", "Impossivel apagar dados."
                                                                     " Erro: {erro}".format(erro=e))
                return

            self.fill_table()
            QMessageBox.information(self, "Sucesso", "Item apagado com sucesso...")


class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.layoutAboutToBeChanged.emit()
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.layoutChanged.emit()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    helloPythonWidget = MainWindow()
    helloPythonWidget.show()

    sys.exit(app.exec_())