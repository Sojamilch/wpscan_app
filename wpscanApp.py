import configparser
import sys
import subprocess
import PyQt5
from PyQt5.QtSql import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView, QTableWidgetItem
from PyQt5.uic import loadUi
import pandas as pd

from package.mainUi import Ui_MainWindow
from package.pandasconverter import DomainsTableModel

class window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.createTableModel()

        ### Detects when button is clicked and runs inputdomain() ###
        #self.addDomain.clicked.connect(self.inputDomain) 

        ### Syncs domain list to latest version of list ###
        self.syncList.clicked.connect(self.createTableModel) 

        ### Starts a manual wpscan of all the websites on the selected day (WIP) ###
        self.initiateManualScan.clicked.connect(self.wpscanManual) 

    def createTableModel(self): ### Creates data model for domain table view ###
        
        ### uses pandas to read he csv file and generate a dataframe/overwrite if re-run ###
        domainList = pd.read_csv('./domains/domains.csv')

        print(domainList.head())

        model = DomainsTableModel(domainList)

        ### Sets the model created by the pandasconverter.py ###
        self.domainTableView.setModel(model)



        #Checks if database exists if not generates it    
        #databaseControlling.databaseCheck(self) 

        #create model for table
        #self.tableModel = QSqlTableModel(self)
        #self.tableModel.setTable("domains")
        #self.tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)

        #Sets header names
        #self.tableModel.setHeaderData(0,  Qt.Horizontal, "ID")
        
            
        #retrieveDataQuery = QSqlQuery("SELECT id, monday,tuesday, wednesday, thursday, friday FROM domains")

        #Retrives data from database and inputs into model (OLD SQLITE METHOD)
        #while retrieveDataQuery.next():
        #    rows = self.tableModel.rowCount()
        #    self.tableModel.insertRow(retrieveDataQuery.value(0))

        #Generate View
        #self.tableModel.select()


        


    #def inputDomain(self): # Adds domains to SQLite database (OLD)
        #databaseControlling.inputDomain(self, str(self.selectDay.currentText()), self.domainInput.text())
        #self.tableModel.select()
        
    def wpscanManual(self):
        subprocess.run('shellScripts/wpscan.sh')



        

        
       



        


# def openDatabaseConnection():
#      #// Reads Database Details//
#     configObject = configparser.RawConfigParser()
#     configObject.read("package/db.ini")
#     connParam = configObject['dbconnection']
    
#     #// Inupts connection data //
#     db = QSqlDatabase.addDatabase('QSQLITE')

#     #// attempts to connect 
#     if not db.open():
#         QMessageBox.critical(
#             None,
#             "table could not connect to databased",
#             "database error: %s" % db.lastError().databaseText(),
#         )            
#         return False
    
 


#     return True
    


if __name__ == '__main__': # Automatically builds the objects when the program is loaded
    
    #if not openDatabaseConnection(): # Attempts to connect to the database 
    #    sys.exit(1)
    
    app = QtWidgets.QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec())
