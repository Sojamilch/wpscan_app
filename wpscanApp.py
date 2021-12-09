import sys

import PyQt5
from PyQt5 import (
    QtGui, 
    QtWidgets, 
    QtCore
   

)
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QMainWindow,
    QTableView

)
from PyQt5.QtSql import (
    QSqlDatabase, 
    QSqlTableModel

)
from package.mainUi import Ui_MainWindow
import configparser

class window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        #create model for table
        self.tableModel = QSqlTableModel(self)
        self.tableModel.setTable("domains")
        self.tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        
        self.tableModel.setHeaderData(0,  Qt.Horizontal, "ID")
        self.tableModel.setHeaderData(1, Qt.Horizontal, "domain name")
        

        self.tableModel.select()

        #Generate View
        self.domainTableView.setModel(self.tableModel)
        self.domainTableView.resizeColumnsToContents()
        


def openDatabaseConnection():
     #// Reads Database Details//
    configObject = configparser.RawConfigParser()
    configObject.read("package/db.ini")
    connParam = configObject['dbconnection']
    
    #// Inupts connection data //
    db = QSqlDatabase.addDatabase('QMARIADB')
    db.setHostName(connParam['servername'])
    db.setDatabaseName(connParam['db'])
    db.setUserName(connParam['username'])
    db.setPassword(connParam['password'])

    
     #// attempts to connect 
    if not db.open():
        QMessageBox.critical(
            None,
            "table could not connect to databased",
            "database error: %s" % db.lastError().databaseText(),
        )            
        return False
    return True
    


    #    self.completed = 0
        
    #//////Testing how to refer to objects and maniplulate////
    #    self.initiateManualScan.clicked.connect(self.increaseProgress)
    #
    #def increaseProgress(self):
    #    
    #    self.completed += 1
    #    self.scanProgressBar.setValue(self.completed)

    #/////////////////////////////////////////////////////////


if __name__ == '__main__': # Automatically builds the objects when the program is loaded
    
    if not openDatabaseConnection():
        sys.exit(1)
    
    app = QtWidgets.QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec())