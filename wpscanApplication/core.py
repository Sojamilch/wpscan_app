import configparser
from email.mime import application
import os
from os.path import exists
from datetime import datetime, timedelta
from re import S
import sys
from time import time
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QProcess, Qt, QThread, QTimer
from mainUi import Ui_MainWindow
from pandascontroller import DomainInput, DomainsTableModel
from apscheduler.schedulers.qt import QtScheduler 

class worker(QtCore.QObject): # Worker object for auto scan

    startScan = QtCore.pyqtSignal(str, str)
    updateConsole = QtCore.pyqtSignal(str)
    updateCurrentDay = QtCore.pyqtSignal(int)
    autoCheck = QtCore.pyqtSignal(bool)
    

    def __init__(self, parent=None):
        super(worker, self).__init__(parent)


 
    def automateScan(self, date): 
        
        scanningSchedule = QtScheduler(timezone="UTC")

        days = ["day1", "day2", "day3", "day4", "day5"]

        weeks = ["Week 1", "Week 2", "Week 3 ", "Week 4"]

        i = 0

        date = date.toPyDate()  
        #print(datetime.utcnow())
        

        startOfWeek = date

        for week in weeks:
            for day in days:
                i += 1

                i = str(i)

                #print(date, datetime.today().strftime("%Y-%m-%d"))
                

                #calculates when each daily job should be executed and adds to scheduler 
                if int(i) == 1 and str(date) == datetime.today().strftime("%Y-%m-%d"):
                    
                    #print("first day")
                    scanningSchedule.add_job(self.startScan.emit, 'interval', args=[f"{day}", f"{week}"], days=28, start_date=date, next_run_time=datetime.utcnow(), id=i)
                else:
                    scanningSchedule.add_job(self.startScan.emit, 'interval', args=[f"{day}", f"{week}"], days=28, start_date=date, id=i)

                date = date + timedelta(days=1)

                i=int(i)

                if i % 5 == 0:
                    date = startOfWeek + timedelta(days=7)
                    startOfWeek = date

        scanningSchedule.start()


        

    


                
            





class window(QtWidgets.QMainWindow, Ui_MainWindow):
    


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        
        
        global thread
        thread = QtCore.QThread(self)
        thread.start()

        self.worker = worker()
        self.worker.moveToThread(thread)
       
        
        self.process = QProcess()
        #Attempts to read the csv

        global domains_path
        global config_path

        domains_name = 'domains/domains.csv'
        config_name = 'shellScripts/wpwatcher.conf'



        if getattr(sys,'frozen',False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        domains_path = os.path.join(application_path, domains_name)
        config_path = os.path.join(application_path, config_name)


    

        try:
            self.data = pd.read_csv(domains_path, dtype=object)   
        except:
            # Adds column headers if none detected
            columnHeaders = ["day1","day2","day3","day4","day5","day1.1","day2.1","day3.1","day4.1","day5.1","day1.2","day2.2","day3.2","day4.2","day5.2","day1.3","day2.3","day3.3","day4.3","day5.3"]    
            self.data = pd.DataFrame(None, columns=columnHeaders, dtype=object)

        # Adds a blank line to the end of the dataframe if there are no rows

        if self.data.shape[0] == 0: 
            self.data = self.data.append(pd.Series(), ignore_index=True)

        self.dateSelector.setMinimumDate(datetime.today())
        
        self.updateDomainList()
        
        ### Detects when button is clicked and runs inputdomain() ###
        self.addDomain.clicked.connect(self.inputDomain) 
        
        self.selectDomainWeek.activated.connect(self.createTableModel)
       
        ### Starts a manual wpscan of all the websites on the selected day (WIP) ###
        self.initiateManualScan.clicked.connect(self.polishedWebList) 

        #Starts auomation
        self.automationEnable.stateChanged.connect(self.isChecked)
  
        self.worker.startScan.connect(self.polishedWebList)

        #displays how long until next scan
        self.worker.updateConsole.connect(self.timeReminaing)

        #detects when scan is finished
        self.process.finished.connect(self.process_end)

        #changes menu
        self.manualToggle.stateChanged.connect(self.changeMenu)

        #Saves config options
        self.saveOptions.clicked.connect(self.saveConfig)

        QTimer.singleShot(1, self.firstTimeSetup)
        

    ### Domain Table View Logic ### 
    
    
    def createTableModel(self): ### Creates data model for domain table view ###
        
        ### uses pandas to read he csv file and generate a dataframe/overwrite if re-run ### #

        if self.selectDomainWeek.currentText() == "Week 1":

            domainListData = self.data.loc[:, "day1":"day5"]

        elif self.selectDomainWeek.currentText() == "Week 2":
            
            domainListData = self.data.loc[:, "day1.1":"day5.1"]

        elif self.selectDomainWeek.currentText() == "Week 3":
            
            domainListData = self.data.loc[:, "day1.2":"day5.2"]

        elif self.selectDomainWeek.currentText() == "Week 4":
            
            domainListData = self.data.loc[:, "day1.3":"day5.3"]

        model = DomainsTableModel(domainListData) # creates the model
        
        ### Sets the model created by the pandasconverter.py ###

        self.domainTableView.setModel(model)
        
        header = self.domainTableView.horizontalHeader()

        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.domainTableView.resizeColumnsToContents()
        model.dataChanged.connect(self.updateDomainList)
  
    def updateDomainList(self): # this is ran when the data in the tabelview changes updating the csv
        self.data.to_csv(domains_path, index=False)
        

    def inputDomain(self): # Adds domains to CSV then refreshes table model with newest version
        
        self.data = DomainInput.input(self, self.domainInput.text(), self.data)
        
        self.createTableModel()

        
    ### End of domain tableview logic ###
    def polishedWebList(self, day=None, week=None):
        #print("weblist")

        if self.manualInput.isHidden():

            if week != None:
                selectedDay = day
                selectedDay = selectedDay.replace(" ", "")
                selectedWeek = week
               
            elif week == None:
                
                selectedDay = self.selectDay.currentText()
                selectedWeek = self.selectWeek.currentText()
                selectedDay = selectedDay.replace(" ", "")

            if selectedWeek == "Week 1":

                domainListData = self.data.loc[:, "day1":"day5"]

            elif selectedWeek == "Week 2":
                
                domainListData = self.data.loc[:, "day1.1":"day5.1"]
                selectedDay = selectedDay + ".1"

            elif selectedWeek == "Week 3":
                
                domainListData = self.data.loc[:, "day1.2":"day5.2"]
                selectedDay = selectedDay + ".2"

            elif selectedWeek == "Week 4":
                
                domainListData = self.data.loc[:, "day1.3":"day5.3"]
                selectedDay = selectedDay + ".3"
            selectedDay = selectedDay.lower()
            listOfWebsites = domainListData[selectedDay].tolist()
        else:
            website = self.manualInput.text()
            listOfWebsites = []
            listOfWebsites.append(website)

        wpConfig = configparser.ConfigParser()
    
        
        

        cleanWebsiteList = []
        
        try: # incase website is invalid value it will just ignore it
            for website in listOfWebsites:
                
                temp = '{"url": '+'"'+ website +'"}'

                cleanWebsiteList.append(temp)
        except:
            pass

        #formatting list to match original reuqirements 
        cleanWebsiteList = ' , '.join(cleanWebsiteList) 
        
        wpConfig.read(config_path) # reading config
        wpConfig['wpwatcher']['wp_sites'] = "[" + cleanWebsiteList + "]"
        
        with open(config_path, 'w') as configFile:
            wpConfig.write(configFile)

        self.wpscan()

    def wpscan(self): # Changes the websites that are going to be run in the config, then executest the scan
        #writes updated config back to file
        absoluteConfigPath = os.path.abspath(config_path) # retrieves path for config location
        self.consoleText.clear()
        self.initiateManualScan.setEnabled(False)
        self.automationEnable.setEnabled(False)
        self.initiateManualScan.setText("...")
        self.process.readyReadStandardOutput.connect(self.wpscanSTDOUT)
        self.process.start("bash", ['shellScripts/wpscan.sh', absoluteConfigPath])
    

        
    def wpscanSTDOUT(self): # Reads console output into log

        output = self.process.readAllStandardOutput()
        text = bytes(output).decode("utf8")
        self.consoleText.append(str(text))
        
    def process_end(self): #destroys process after execution and changes button text
       
        self.initiateManualScan.setText("Done!")
        QTimer.singleShot(2000, lambda: self.initiateManualScan.setText("SCAN"))
        self.initiateManualScan.setEnabled(True)
        self.automationEnable.setEnabled(True)
     
    def timeReminaing(self, text):
        self.consoleText.append(str(text))

    def isChecked(self):
        
        if self.automationEnable.isChecked() and self.initiateManualScan.isEnabled():
            self.worker.automateScan(self.dateSelector.date())
            self.dateSelector.setEnabled(False)
            
        else:
            self.process.kill()
            self.dateSelector.setEnabled(True)
            self.consoleText.append("Process Killed mid execution....")


    def closeEvent(self, event): # Warns user when trying to close program
        questionBox = QtWidgets.QMessageBox

        if self.automationEnable.isChecked() or self.process.state() == 2:
            answer = questionBox.question(self, '', "Are you sure you want to close? \n You will cancel the current schedule!", questionBox.Yes | questionBox.No)

        if answer == questionBox.Yes:
         
            event.accept()
        else:

            event.ignore()

    def changeMenu(self):
        if self.manualInput.isHidden():
            self.manualInput.show()
            self.selectWeek.hide()
            self.selectDay.hide()
        else:
            self.manualInput.hide()
            self.selectWeek.show()
            self.selectDay.show()

    def firstTimeSetup(self): #Ask for setup on first time running
        
        self.createTableModel()

        if not exists(config_path):
            os.system("wpwatcher --template_conf > shellScripts/wpwatcher.conf")
            fileCheck = QtWidgets.QMessageBox()
            answer = fileCheck.question(self,"Setup","Please configure the scanner to continue...", fileCheck.Yes | fileCheck.No)

            if answer == fileCheck.Yes:
                self.tabWidget.setCurrentIndex(3)
            else:
                pass
        
        #reads config file to options Page
        reader = configparser.ConfigParser()

        reader.read(config_path)
        emailAdress = reader["wpwatcher"]["email_to"]
        emailAdress = emailAdress.strip('["]')
        self.emailTo.setText(emailAdress) 
        self.emailFrom.setText(reader["wpwatcher"]["from_email"])
        self.smtpServer.setText(reader["wpwatcher"]["smtp_server"])
        self.passwordBox.setText(reader["wpwatcher"]["smtp_pass"])
        if reader["wpwatcher"]["send_email_report"] == "Yes":
            self.emailReport.setChecked(True)
        else:
            self.emailReport.setChecked(False)  

    def saveConfig(self):
        config = configparser.ConfigParser()

        config.read(config_path) # reading config
        if self.emailReport.isChecked():
            config["wpwatcher"]["send_email_report"] = "Yes"
        else:
            config["wpwatcher"]["send_email_report"] = "No"
        
        apiKeyFormatted = '[ "--format","json","--random-user-agent", "--api-token", "'  + self.apiKeyBox.text() + '"]'

        config["wpwatcher"]["email_to"] = '["' + self.emailTo.text() + '"]'
        config["wpwatcher"]["from_email"] = self.emailFrom.text()
        config["wpwatcher"]["smtp_server"] = self.smtpServer.text()
        config["wpwatcher"]["smtp_user"] = self.emailFrom.text()
        config["wpwatcher"]["smtp_pass"] = self.passwordBox.text()
        config["wpwatcher"]["wpscan_args"] = apiKeyFormatted

        with open(config_path, 'w') as configFile:
            config.write(configFile)

        saveComplete = QtWidgets.QMessageBox()
        saveComplete.about(self,"Success!","Options saved to wpwatcher.conf!")



if __name__ == '__main__': # Automatically builds the objects when the program is loaded
    
    app = QtWidgets.QApplication(sys.argv)
    win = window()
    win.show()
    app.exec()
   