# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wpscan.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
# Generates all the objects for the UI elements


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QFormLayout, QGroupBox, QHBoxLayout)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 800, 400))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())

        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.scanTab = QtWidgets.QWidget()
        self.scanTab.setObjectName("scanTab")

        self.initiateManualScan = QtWidgets.QPushButton(self.scanTab)
        self.initiateManualScan.setGeometry(QtCore.QRect(300, 70, 200, 100))
        font = QtGui.QFont()
        font.setPointSize(45)
        self.initiateManualScan.setFont(font)
        self.initiateManualScan.setIconSize(QtCore.QSize(16, 16))
        self.initiateManualScan.setObjectName("initiateManualScan")

        self.automationEnable = QtWidgets.QCheckBox(self.scanTab)
        self.automationEnable.setGeometry(QtCore.QRect(350, 220, 101, 23))
        self.automationEnable.setObjectName("automationEnable")

      #  self.scanProgressBar = QtWidgets.QProgressBar(self.scanTab)
     #   self.scanProgressBar.setGeometry(QtCore.QRect(340, 190, 120, 25))
    #    self.scanProgressBar.setProperty("value", 0)
   #     self.scanProgressBar.setObjectName("scanProgressBar")


        self.tabWidget.addTab(self.scanTab, "")
        self.domainList = QtWidgets.QWidget()
        self.domainList.setObjectName("domainList")

        self.domainTableView = QtWidgets.QTableView(self.domainList)
        self.domainTableView.setGeometry(QtCore.QRect(10, 140, 775, 200))
        self.domainTableView.setObjectName("domainTableView")
        self.domainTableView.horizontalHeader().setCascadingSectionResizes(False)
        self.domainTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        self.domainInput = QtWidgets.QLineEdit(self.domainList)
        self.domainInput.setPlaceholderText("https://www.wordpressite.com")
        self.domainInput.setGeometry(QtCore.QRect(10, 30, 270, 25))
        self.domainInput.setObjectName("domainInput")

        self.label = QtWidgets.QLabel(self.domainList)
        self.label.setGeometry(QtCore.QRect(10, 10, 91, 17))
        self.label.setObjectName("label")

        self.addDomain = QtWidgets.QPushButton(self.domainList)
        self.addDomain.setGeometry(QtCore.QRect(290, 30, 100, 25))
        self.addDomain.setObjectName("addDomain")
        
        self.syncList = QtWidgets.QPushButton(self.domainList)
        self.syncList.setGeometry(QtCore.QRect(685, 110, 100, 25))
        self.syncList.setObjectName("syncList")
        
        self.selectWeek = QtWidgets.QComboBox(self.scanTab) # scantab week selection
        self.selectWeek.setGeometry(QtCore.QRect(300, 260, 200, 26))
        self.selectWeek.setObjectName("selectWeek")
        self.selectWeek.addItem("Week 1")
        self.selectWeek.addItem("Week 2")
        self.selectWeek.addItem("Week 3")
        self.selectWeek.addItem("Week 4")
    

        self.selectDay = QtWidgets.QComboBox(self.scanTab) # scantab day selection 
        self.selectDay.setGeometry(QtCore.QRect(300, 300, 200, 26))
        self.selectDay.setObjectName("selectDay")
        self.selectDay.addItem("Monday")
        self.selectDay.addItem("Tuesday")
        self.selectDay.addItem("Wednesday")
        self.selectDay.addItem("Thursday")
        self.selectDay.addItem("Friday")
    

        self.selectDomainWeek = QtWidgets.QComboBox(self.domainList) # domain list viewing
        self.selectDomainWeek.setGeometry(QtCore.QRect(10, 110, 100, 25))
        self.selectDomainWeek.setObjectName("selectDomainWeek")
        self.selectDomainWeek.addItem("Week 1")
        self.selectDomainWeek.addItem("Week 2")
        self.selectDomainWeek.addItem("Week 3")
        self.selectDomainWeek.addItem("Week 4")

        self.tabWidget.addTab(self.domainList, "")

        self.logPage = QtWidgets.QWidget()
        self.logPage.setObjectName("logPage")

        self.tabWidget.addTab(self.logPage, "")
        MainWindow.setCentralWidget(self.centralwidget)



        # for i in range(0,4):
        #     weeks = [self.week1,self.week2,self.week3,self.week4]
        #     weeks[i].setChecked(True)
        #     weeks[i].setStyleSheet("""
        #     QCheckBox::Indicator {
        #         width: 25px;
        #         height: 25px;
        #     }
        #     """)

        

        self.logBox = QtWidgets.QGroupBox("Scan Log",self.logPage)
        consoleBox = QtWidgets.QHBoxLayout(self.logPage)
        self.consoleText = QtWidgets.QTextEdit(self.logPage)
        consoleBox.addWidget(self.consoleText)

        #self.cursor = QtWidgets.QTextCursor(self.consoleText.document())
        


        self.consoleText.setReadOnly(True)
        self.logBox.setLayout(consoleBox)
        self.logBox.setGeometry(0,10,790,300)

        
    
        #Options Page for config
        self.optionsPage = QtWidgets.QWidget()
        self.optionsPage.setObjectName("optionsPage")
        self.tabWidget.addTab(self.optionsPage, "")

        self.optionsBox = QtWidgets.QVBoxLayout(self.optionsPage)

        self.passwordBox = QtWidgets.QLineEdit()
        self.passwordBox.setEchoMode(QtWidgets.QLineEdit.Password)

        self.emailReport = QtWidgets.QCheckBox()

        self.emailTo = QtWidgets.QLineEdit()

        self.emailFrom = QtWidgets.QLineEdit()

        self.smtpServer = QtWidgets.QLineEdit()

        self.apiKeyBox = QtWidgets.QLineEdit()

        self.saveOptions = QtWidgets.QPushButton()
        self.saveOptions.setFixedSize(QtCore.QSize(100,25))

        self.configForm = QGroupBox("Options", self.optionsPage)
        layout = QFormLayout()
        layout.addRow(QtWidgets.QLabel("Send Email Report?"), self.emailReport)
        layout.addRow(QtWidgets.QLabel("Email to:"), self.emailTo)
        layout.addRow(QtWidgets.QLabel("Email from:"), self.emailFrom)
        layout.addRow(QtWidgets.QLabel("SMTP Server: "), self.smtpServer)
        layout.addRow(QtWidgets.QLabel("Sender Password: "), self.passwordBox)
        layout.addRow(QtWidgets.QLabel("WPSCAN API Key: "), self.apiKeyBox)
        layout.addRow(self.saveOptions)
        

        self.configForm.setLayout(layout)
        

        self.optionsBox.addWidget(self.configForm)
        
        self.optionsBox.setGeometry(QtCore.QRect(50,25,100,100))

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        self.menuWordPress_Scan = QtWidgets.QMenu(self.menubar)
        self.menuWordPress_Scan.setObjectName("menuWordPress_Scan")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Wordpress Vunerabiltiy Scanner"))
        self.initiateManualScan.setText(_translate("MainWindow", "SCAN"))
        self.automationEnable.setText(_translate("MainWindow", "Automate?"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.scanTab), _translate("MainWindow", "Scan"))
        #self.domainInput.setText(_translate("MainWindow", ''))
        self.label.setText(_translate("MainWindow", "Add Domain"))
        self.addDomain.setText(_translate("MainWindow", "Add domain"))
        self.syncList.setText(_translate("MainWindow", "Sync List"))
        self.saveOptions.setText(_translate("MainWindow", "Save Options"))
        
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.domainList), _translate("MainWindow", "Domains"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.logPage), _translate("MainWindow", "Log"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.optionsPage), _translate("MainWindow", "Options"))
        self.menuWordPress_Scan.setTitle(_translate("MainWindow", "WordPress Scanner"))


if __name__ == '__main__':
    window = Ui_MainWindow()
    Ui_MainWindow.setupUi
