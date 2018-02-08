from PyQt5 import QtSql, QtWidgets
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtSql import QSqlQuery, QSqlTableModel
from PyQt5.QtSql import QSqlDriver

filename = 'tasks.tsdb'

class DBCOnnection(QSqlDatabase):

    def __init__(self, file=None):

        super(DBCOnnection, self).__init__(file)
        file = filename
        self.db = self.addDatabase('QSQLITE')
        self.db.setDatabaseName(file)

        if not self.db.open():
            QtWidgets.QMessageBox.critical(None, QtWidgets.qApp.tr("Cannot open database"),
                                       QtWidgets.qApp.tr("Unable to establish a database connection.\n"
                                                     "This example needs SQLite support. Please read "
                                                     "the Qt SQL driver documentation for information "
                                                     "how to build it.\n\n" "Click Cancel to exit."),
                                       QtWidgets.QMessageBox.Cancel)
            return

    def insert(self, table_name, fields, values):

        sql = "INSERT OR IGNORE INTO {tn} ({flds}) VALUES ({vls})".format(tn=table_name, flds=fields, vls=values)
        query = QSqlQuery()
        query.exec_(sql)

    def insert(self, table_name, values):

        sql = "INSERT OR IGNORE INTO {tn} VALUES ({vls})".format(tn=table_name, vls=values)

        print(sql)
        query = QSqlQuery()
        query.exec_(sql)

    def update(self, table_name, values, condition):
        sql = "UPDATE {tn} set {vls} where {cond}".format(tn=table_name, vls=values, cond=condition)

        query = QSqlQuery()

        print(sql)
        try:
           query.exec_(sql)
        except query.lastError() as e:
            return

    def delete(self, table_name, condition):
        sql = "DELETE FROM {tn} where {cond}".format(tn=table_name, cond=condition)

        query = QSqlQuery()

        try:
            query.exec_(sql)
        except query.lastError() as e:
            return

    def mostrarRegisto(self, tabela, condition, field):
        model = QSqlTableModel()
        model.setTable(tabela)
        model.setFilter(condition)
        model.select()

        return model.record(0).value(field)

