import configparser
import os
import subprocess
import sys
from calendar import c, week, weekday

import numpy
import pandas as pd
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox,
                             QTableView, QTableWidgetItem, QStyleFactory)
from PyQt5.uic import loadUi

from mainUi import Ui_MainWindow
from pandascontroller import DomainInput, DomainsTableModel


class window(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        #self.wpScan = QtCore.QProcess(self)
        #self.wpScan.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        


        self.weekList = {

            "Week 2":".1",
            "Week 3":".2",
            "Week 4":".3"

        }   

        #Attempts to read the csv
        try:
            self.data = pd.read_csv('../domains/domains.csv', dtype=object)   
        except:
            # Adds column headers if none detected
            columnHeaders = ["monday","tuesday","wednesday","thursday","friday","monday.1","tuesday.1","wednesday.1","thursday.1","friday.1","monday.2","tuesday.2","wednesday.2","thursday.2","friday.2","monday.3","tuesday.3","wednesday.3","thursday.3","friday.3"]    
            self.data = pd.DataFrame(None, columns=columnHeaders)

        # Adds a blank line to the end of the dataframe if there are no rows

        if self.data.shape[0] == 0: 
            self.data = self.data.append(pd.Series(), ignore_index=True)


        #if self.data.shape[0] == 0: # Adds a blank line to the end of the dataframe if there are no rows
         #   self.data = self.data.append(pd.Series(), ignore_index=True)
            
        self.updateDomainList()
        
        ### Detects when button is clicked and runs inputdomain() ###
        self.addDomain.clicked.connect(self.inputDomain) 
        
        self.selectDomainWeek.activated.connect(self.createTableModel)


        ### Syncs domain list to latest version of list ###
        
        #self.syncList.clicked.connect(self.updateDomainList) 
       

        ### Starts a manual wpscan of all the websites on the selected day (WIP) ###
        self.initiateManualScan.clicked.connect(self.wpscanManual) 


        #self.wpScan.readyRead.connect(self.onReadReady)
         

    
    ### Domain Table View Logic ### 
    
    
    def createTableModel(self): ### Creates data model for domain table view ###
        
        ### uses pandas to read he csv file and generate a dataframe/overwrite if re-run ### #

        if self.selectDomainWeek.currentText() == "Week 1":

            domainListData = self.data.loc[:, "monday":"friday"]

        elif self.selectDomainWeek.currentText() == "Week 2":
            
            domainListData = self.data.loc[:, "monday.1":"friday.1"]

        elif self.selectDomainWeek.currentText() == "Week 3":
            
            domainListData = self.data.loc[:, "monday.2":"friday.2"]

        elif self.selectDomainWeek.currentText() == "Week 4":
            
            domainListData = self.data.loc[:, "monday.3":"friday.3"]
        


        model = DomainsTableModel(domainListData) # creates the model
        
        ### Sets the model created by the pandasconverter.py ###

        self.domainTableView.setModel(model)
        
        header = self.domainTableView.horizontalHeader()

        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        model.dataChanged.connect(self.updateDomainList)
  

    def updateDomainList(self): # this is ran when the data in the tabelview changes updating the csv

        print(self.data)

        self.data.to_csv("../domains/domains.csv", index=False)

        print("wrote to csv.")
        

    def inputDomain(self): # Adds domains to CSV then refreshes table model with newest version
        
        #self.updateDomainList()
        self.data = DomainInput.input(self, self.domainInput.text(), self.data)
        
        self.createTableModel()

      
        
    ### End of domain tableview logic ###




    def wpscanManual(self): # Changes the websites that are going to be run in the config, then executest the scan

        wpConfig = configparser.ConfigParser()
        
        wpConfig.read('../shellScripts/wpwatcher.conf') # reading config
        print(wpConfig['wpwatcher']['wp_sites'])

        selectedDay = self.selectDay.currentText()
        selectedDay = selectedDay.lower() # for which day to manually scan
        
        listOfWebsites = self.data[selectedDay].tolist()

        cleanWebsiteList = []
        
        try: # incase website is invalid value it will just ignore it
            for website in listOfWebsites:
                
                temp = '{"url": '+'"'+ website +'"}'

                cleanWebsiteList.append(temp)
        except:
            print("null value")

        
        #formatting list to match original reuqirements 
        cleanWebsiteList = ' , '.join(cleanWebsiteList) 
        print(cleanWebsiteList)
        wpConfig['wpwatcher']['wp_sites'] = "[" + cleanWebsiteList + "]"

        print(wpConfig['wpwatcher']['wp_sites'])

        with open('../shellScripts/wpwatcher.conf', 'w') as configFile:
            wpConfig.write(configFile)

        #writes updated config back to file

        absoluteConfigPath = os.path.abspath("../shellScripts/wpwatcher.conf") # retrieves path for config location

        self.consoleText.clear()

        
        #self.wpScan.setArguments([absoluteConfigPath])
        #self.wpScan.start('../shellScripts/wpwatcher.conf')
        output = subprocess.Popen(['bash', '../shellScripts/wpscan.sh', absoluteConfigPath], stdout=subprocess.PIPE)
        
        while True:
            line = output.stdout.readline()
            if not line:
                break
            
            
            line = line.rstrip()
            line = line.decode()
            line += '\n'
            self.consoleText.append(str(line))
            #self.cursor.setPosition(-1)
            #self.consoleText.setTextCursor(self.cursor)

            #self.consoleText.insertPlainText(str(line))
         # executes script
        

    #def onReadReady(self):
    #    output = self.wpScan.readAllStandardOutput().data().decode()
    #    self.consoleText.append(output)

        #subprocess.run(['bash', '../shellScripts/wpscan.sh', absoluteConfigPath]) # executes script



if __name__ == '__main__': # Automatically builds the objects when the program is loaded
    
    
    app = QtWidgets.QApplication(sys.argv)

    win = window()
    win.show()
    sys.exit(app.exec())
   