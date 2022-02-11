
import configparser
import os
import datetime
from re import S
#import subprocess
import sys
from tkinter.tix import Tree
from numpy import diff
from pyrsistent import s
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


class worker(QtCore.QObject): # Worker object for auto scan

    startScan = QtCore.pyqtSignal(str, str)
    updateConsole = QtCore.pyqtSignal(str)
    updateCurrentDay = QtCore.pyqtSignal(int)
    autoCheck = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(worker, self).__init__(parent)
        self.currentDay = 0
        self.updateCurrentDay.connect(self.updateDay)
        
        
    def updateDay(self):
        self.currentDay += 1
    
    def automationCheck(self, tick):
        print(self.check)
        self.check = tick
        return self.check
        

    @freeze_time("2022-02-14", as_kwarg='test3')
    def automateScan(self, test3): 
        
        # if window.findNextMonday(win) != 0:
        #     print(window.findNextMonday(win))
        #     print("its not monday yet", datetime.date.today())
        #     window.thread.sleep(window.findNextMonday(win))
        #
         
        print("executing")
        if self.findNextMonday() == 0 and self.currentDay == 0:
            print("week 1")
            schedule.clear()

            #window.polishedWebList(win,"monday","Week 1")
            self.startScan.emit("monday", "Week 1")
            schedule.every().tuesday.do(self.startScan.emit, "tuesday", "Week 1")
            schedule.every().wednesday.do(self.startScan.emit, "wednesday", "Week 1")
            schedule.every().thursday.do(self.startScan.emit, "thursday", "Week 1")
            schedule.every().friday.do(self.startScan.emit, "friday", "Week 1")

        elif self.currentDay == 5:
            schedule.clear()
            self.startScan.emit("monday", "Week 2")
            schedule.every().tuesday.do(self.startScan.emit, "tuesday", "Week 2")
            schedule.every().wednesday.do(self.startScan.emit, "wednesday", "Week 2")
            schedule.every().thursday.do(self.startScan.emit, "thursday", "Week 2")
            schedule.every().friday.do(self.startScan.emit, "friday", "Week 2")

        elif self.currentDay == 10:
            self.startScan.emit("monday", "Week 3")
            schedule.every().tuesday.do(self.startScan.emit, "tuesday", "Week 3")
            schedule.every().wednesday.do(self.startScan.emit, "wednesday", "Week 3")
            schedule.every().thursday.do(self.startScan.emit, "thursday", "Week 3")
            schedule.every().friday.do(self.startScan.emit, "friday", "Week 3")

        elif self.currentDay == 15:
            self.startScan.emit("monday", "Week 4")
            schedule.every().tuesday.do(self.startScan.emit, "tuesday", "Week 4")
            schedule.every().wednesday.do(self.startScan.emit, "wednesday", "Week 4")
            schedule.every().thursday.do(self.startScan.emit, "thursday", "Week 4")
            schedule.every().friday.do(self.startScan.emit, "friday", "Week 4")

    @freeze_time("2022-02-14", as_kwarg='test1')
    def findNextMonday(self, test1):
        print("finding date")
        today = datetime.date.today()
        
        comingMonday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
        
        difference = comingMonday - today

        totalSeconds = difference.total_seconds()

        print(today)
        print(today.weekday())
        if today.weekday() == 0:
            print(today.weekday())
            return today.weekday()
        else:
            return totalSeconds

   
    def confAutomation(self):
            print("ok starting")
            if self.findNextMonday() != 0:
                secondsRemaining = int((self.findNextMonday()*1000))
                print("Its not monday yet", secondsRemaining)
                self.updateConsole.emit("Waiting: " + str(secondsRemaining) + " seconds")
            else:
                self.automateScan()
                
            





class window(QtWidgets.QMainWindow, Ui_MainWindow):
    


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


        
        global thread
        thread = QtCore.QThread(self)
        thread.start()

 
        self.worker = worker()
        self.worker.moveToThread(thread)
        print(self.worker.thread())
        
        self.process = QProcess()
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

        self.automationEnable.stateChanged.connect(self.isChecked)
  
        self.worker.startScan.connect(self.polishedWebList)

        self.worker.updateConsole.connect(self.timeReminaing)

        self.process.finished.connect(self.process_end)

#        self.destroyed.connect(self.isDestroyed)

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
        
        if day is not None:
            selectedDay = day
            selectedWeek = week
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
        print("Finished cleaning")
        self.wpscan()

    def wpscan(self): # Changes the websites that are going to be run in the config, then executest the scan
        print("scanning")
        #writes updated config back to file
        absoluteConfigPath = os.path.abspath("../shellScripts/wpwatcher.conf") # retrieves path for config location
        self.consoleText.clear()
        self.initiateManualScan.setEnabled(False)
        self.initiateManualScan.setText("...")
        self.process.readyReadStandardOutput.connect(self.wpscanSTDOUT)
        self.process.start("bash", ['../shellScripts/wpscan.sh', absoluteConfigPath])

        
    def wpscanSTDOUT(self): # Reads console output into log
        output = self.process.readAllStandardOutput()
        text = bytes(output).decode("utf8")
        self.consoleText.append(str(text))
        
    def process_end(self): #destroys process after execution and changes button text
        print("Finsihed...")
        #self.process = None
        self.initiateManualScan.setText("Done!")
        QTimer.singleShot(2000, lambda: self.initiateManualScan.setText("SCAN"))
        self.initiateManualScan.setEnabled(True)
     
    def timeReminaing(self, text):
        self.consoleText.append(str(text))

    def isChecked(self):
        
        if self.automationEnable.isChecked() and self.initiateManualScan.isEnabled():
            try:
                #self.worker = worker()
                #self.worker.moveToThread(thread)
                print("created worker")
            except:
                pass
            self.worker.confAutomation()
        else:
            self.process.kill()
            self.consoleText.append("Process Killed mid execution....")
            print(self.worker.thread())
            print("Deleted Worker - re-created worker")


    
if __name__ == '__main__': # Automatically builds the objects when the program is loaded
    
    
    app = QtWidgets.QApplication(sys.argv)

    win = window()
    win.show()
    sys.exit(app.exec())
   