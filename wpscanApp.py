import configparser
import subprocess
import sys

import numpy
import pandas as pd
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox,
                             QTableView, QTableWidgetItem)
from PyQt5.uic import loadUi

from package.mainUi import Ui_MainWindow
from package.pandasconverter import DomainInput, DomainsTableModel


class window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    

        self.createTableModel()
        

        ### Detects when button is clicked and runs inputdomain() ###
        self.addDomain.clicked.connect(self.inputDomain) 

        ### Syncs domain list to latest version of list ###
        self.syncList.clicked.connect(self.createTableModel) 

        ### Starts a manual wpscan of all the websites on the selected day (WIP) ###
        self.initiateManualScan.clicked.connect(self.wpscanManual) 

    def createTableModel(self): ### Creates data model for domain table view ###
        
        ### uses pandas to read he csv file and generate a dataframe/overwrite if re-run ###
        
        data = pd.read_csv('./domains/domains.csv')
        
        print(data.head())

        model = DomainsTableModel(data)

        ### Sets the model created by the pandasconverter.py ###
        self.domainTableView.setModel(model)



    def inputDomain(self): # Adds domains to CSV
        data = pd.read_csv('./domains/domains.csv')
        DomainInput.input(self, str(self.selectDay.currentText()), self.domainInput.text(), data)
        #self.tableModel.select()
        
    def wpscanManual(self):
        subprocess.run('shellScripts/wpscan.sh')
    


if __name__ == '__main__': # Automatically builds the objects when the program is loaded
    
    
    app = QtWidgets.QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec())
