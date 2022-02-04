
import configparser
import os
import datetime
#import subprocess
import sys
from numpy import diff
#from calendar import c, week, weekday
#from time import sleep
import schedule
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QProcess, Qt, QThread, QTimer
#from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox,
#                             QStyleFactory, QTableView, QTableWidgetItem)
#from PyQt5.uic import loadUi

from mainUi import Ui_MainWindow
from pandascontroller import DomainInput, DomainsTableModel

#TESTING 
from freezegun import freeze_time




class window(QtWidgets.QMainWindow, Ui_MainWindow):
    currentDay = 0
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        window.currentDay = 0 
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

            
        self.updateDomainList()
        
        ### Detects when button is clicked and runs inputdomain() ###
        self.addDomain.clicked.connect(self.inputDomain) 
        
        self.selectDomainWeek.activated.connect(self.createTableModel)


        ### Syncs domain list to latest version of list ###
        
        #self.syncList.clicked.connect(self.updateDomainList) 
       

        ### Starts a manual wpscan of all the websites on the selected day (WIP) ###
        self.initiateManualScan.clicked.connect(self.polishedWebList) 

        self.automationEnable.stateChanged.connect(self.createThread)

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

        #print(self.data)

        self.data.to_csv("../domains/domains.csv", index=False)

        #print("wrote to csv.")
        

    def inputDomain(self): # Adds domains to CSV then refreshes table model with newest version
        
        self.data = DomainInput.input(self, self.domainInput.text(), self.data)
        
        self.createTableModel()

        
    ### End of domain tableview logic ###
    def polishedWebList(self, day=None, week=None):
        
        if day is None:
            selectedDay = day
            selectedWeek = week
            self.currentDay += 1
            print(self.currentDay)
        else:
            selectedDay = self.selectDay.currentText()
            selectedWeek = self.selectWeek.currentText()

        if selectedWeek == "Week 1":

            domainListData = self.data.loc[:, "monday":"friday"]

        elif selectedWeek == "Week 2":
            
            domainListData = self.data.loc[:, "monday.1":"friday.1"]
            selectedDay = selectedDay + ".1"

        elif selectedWeek == "Week 3":
            
            domainListData = self.data.loc[:, "monday.2":"friday.2"]
            selectedDay = selectedDay + ".2"

        elif selectedWeek == "Week 4":
            
            domainListData = self.data.loc[:, "monday.3":"friday.3"]
            selectedDay = selectedDay + ".3"
            
        wpConfig = configparser.ConfigParser()
        
        wpConfig.read('../shellScripts/wpwatcher.conf') # reading config
        #print(wpConfig['wpwatcher']['wp_sites'])

        selectedDay = selectedDay.lower()
        listOfWebsites = domainListData[selectedDay].tolist()
        print(selectedDay, listOfWebsites)

        cleanWebsiteList = []
        
        try: # incase website is invalid value it will just ignore it
            for website in listOfWebsites:
                
                temp = '{"url": '+'"'+ website +'"}'

                cleanWebsiteList.append(temp)
        except:
            pass

        #formatting list to match original reuqirements 
        cleanWebsiteList = ' , '.join(cleanWebsiteList) 
        #print(cleanWebsiteList)
        wpConfig['wpwatcher']['wp_sites'] = "[" + cleanWebsiteList + "]"

        #print(wpConfig['wpwatcher']['wp_sites'])

        with open('../shellScripts/wpwatcher.conf', 'w') as configFile:
            wpConfig.write(configFile)

        self.wpscan()

    def wpscan(self): # Changes the websites that are going to be run in the config, then executest the scan
        
        #writes updated config back to file
        self.process = QProcess() #creates thread for scanning
        absoluteConfigPath = os.path.abspath("../shellScripts/wpwatcher.conf") # retrieves path for config location
        self.consoleText.clear()
        self.initiateManualScan.setEnabled(False)
        self.initiateManualScan.setText("...")
        self.process.finished.connect(self.process_end)
        self.process.readyReadStandardOutput.connect(self.wpscanSTDOUT)
        self.process.start("bash", ['../shellScripts/wpscan.sh', absoluteConfigPath])
        
    def wpscanSTDOUT(self): # Reads console output into log
        output = self.process.readAllStandardOutput()
        text = bytes(output).decode("utf8")
        self.consoleText.append(str(text))
        
    def process_end(self): #destroys thread after execution and changes button text
        self.process = None
        self.initiateManualScan.setText("Done!")
        QTimer.singleShot(2000, lambda: self.initiateManualScan.setText("SCAN"))
        self.initiateManualScan.setEnabled(True)

    def findNextMonday(self):
        today = datetime.date.today()
        comingMonday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
        
        difference = comingMonday - today

        totalSeconds = difference.total_seconds()


        if today.weekday() == 1:
            return today.weekday()
        else:
            return totalSeconds
                
    def createThread(self):

        if self.automationEnable.isChecked():
            window.currentDay = 0
            self.thread = WorkerThread()
            self.thread.start()
            print("openedThread")

        if self.automationEnable.isChecked() == False:
            self.thread.exit()
            print("closed thread")



class WorkerThread(QThread):
    @freeze_time("2022-02-14", as_kwarg='test')
    def run(self, test): 
        if window.findNextMonday(win) != 0:
            print(window.findNextMonday(win))
            print("its not monday yet", datetime.date.today())
            window.thread.sleep(window.findNextMonday(win))
            
        if window.findNextMonday() == 0:
            print("week 1")
            schedule.clear()
            for index in range(window.selectedDay.count()):
                day = window.selectedDay.itemText(index)
                day = day.lower()
                schedule.every().day.do(window.polishedWebList(self,day,"Week 1"))
        
        elif window.currentDay == 5:
            print("week 2")
            schedule.clear()
            for index in range(window.selectedDay.count()):
                day = window.selectedDay.itemText(index)
                day = day.lower()
                schedule.every().day.do(window.polishedWebList(self,day,"Week 2"))

        elif window.currentDay == 10:
            schedule.clear()
            for index in range(window.selectedDay.count()):
                day = window.selectedDay.itemText(index)
                day = day.lower()
                schedule.every().day.do(window.polishedWebList(self,day,"Week 3"))

        elif window.currentDay == 15:
            schedule.clear()
            for index in range(window.selectedDay.count()):
                day = window.selectedDay.itemText(index)
                day = day.lower()
                schedule.every().day.do(window.polishedWebList(self,day,"Week 4"))

        

    
if __name__ == '__main__': # Automatically builds the objects when the program is loaded
    
    
    app = QtWidgets.QApplication(sys.argv)

    win = window()
    win.show()
    sys.exit(app.exec())
   