import configparser
import sys
import subprocess
import PyQt5
from PyQt5.QtSql import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView, QTableWidgetItem
from PyQt5.uic import loadUi

from package.mainUi import Ui_MainWindow
from package.databaseMigration import databaseCheck

class window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.createTableModel()

        self.addDomain.clicked.connect(self.inputDomain) # Detects when button is clicked
        self.syncList.clicked.connect(self.createTableModel) # Syncs domain list to latest version of list
        self.initiateManualScan.clicked.connect(self.wpscanManual) # Starts a manual wpscan of all the websites on the selected day

    def createTableModel(self): # Creates data model for domain table view
        


        #Checks if database exists if not generates it    
        databaseCheck() 

        #create model for table
        self.tableModel = QSqlTableModel(self)
        self.tableModel.setTable("domains")
        self.tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)

        #Sets header names
        self.tableModel.setHeaderData(0,  Qt.Horizontal, "ID")
        
            
        retrieveDataQuery = QSqlQuery("SELECT id, monday,tuesday, wednesday, thursday, friday FROM domains")

        #Retrives data from database and inputs into model
        while retrieveDataQuery.next():
            rows = self.tableModel.rowCount()
            self.tableModel.insertRow(retrieveDataQuery.value(0))

        #Generate View
        self.tableModel.select()
        self.domainTableView.setModel(self.tableModel)
        #Resize Columns
        self.domainTableView.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

    def inputDomain(self): # Adds domains to SQLite database
        inputDay = ''



        inputDomainQuery = QSqlQuery()

        inputDomainQuery.prepare(
            """
            INSERT INTO domains (
                domain
            )
            VALUES (?)
            """
        )

        inputDomainQuery.addBindValue(self.domainInput.text())
        inputDomainQuery.exec()
        
    def wpscanManual(self):
        subprocess.run('shellScripts/wpscan.sh')



        

        
       



        


def openDatabaseConnection():
     #// Reads Database Details//
    configObject = configparser.RawConfigParser()
    configObject.read("package/db.ini")
    connParam = configObject['dbconnection']
    
    #// Inupts connection data //
    db = QSqlDatabase.addDatabase('QSQLITE')

    #// attempts to connect 
    if not db.open():
        QMessageBox.critical(
            None,
            "table could not connect to databased",
            "database error: %s" % db.lastError().databaseText(),
        )            
        return False
    
 


    return True
    


if __name__ == '__main__': # Automatically builds the objects when the program is loaded
    
    if not openDatabaseConnection(): # Attempts to connect to the database 
        sys.exit(1)
    
    app = QtWidgets.QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec())
