# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wpscan.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
# Generates all the objects for the UI elements


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(400, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 400, 400))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.scanTab = QtWidgets.QWidget()
        self.scanTab.setObjectName("scanTab")
        self.initiateManualScan = QtWidgets.QPushButton(self.scanTab)
        self.initiateManualScan.setGeometry(QtCore.QRect(100, 100, 200, 100))
        font = QtGui.QFont()
        font.setPointSize(45)
        self.initiateManualScan.setFont(font)
        self.initiateManualScan.setIconSize(QtCore.QSize(16, 16))
        self.initiateManualScan.setObjectName("initiateManualScan")
        self.automationEnable = QtWidgets.QCheckBox(self.scanTab)
        self.automationEnable.setGeometry(QtCore.QRect(150, 250, 101, 23))
        self.automationEnable.setObjectName("automationEnable")
        self.scanProgressBar = QtWidgets.QProgressBar(self.scanTab)
        self.scanProgressBar.setGeometry(QtCore.QRect(140, 210, 120, 25))
        self.scanProgressBar.setProperty("value", 24)
        self.scanProgressBar.setObjectName("scanProgressBar")
        self.tabWidget.addTab(self.scanTab, "")
        self.domainList = QtWidgets.QWidget()
        self.domainList.setObjectName("domainList")
        self.domainTableView = QtWidgets.QTableView(self.domainList)
        self.domainTableView.setGeometry(QtCore.QRect(10, 140, 380, 200))
        self.domainTableView.setObjectName("domainTableView")
        self.domainTableView.horizontalHeader().setCascadingSectionResizes(False)
        self.domainInput = QtWidgets.QLineEdit(self.domainList)
        self.domainInput.setGeometry(QtCore.QRect(10, 30, 270, 25))
        self.domainInput.setObjectName("domainInput")
        self.label = QtWidgets.QLabel(self.domainList)
        self.label.setGeometry(QtCore.QRect(10, 10, 91, 17))
        self.label.setObjectName("label")
        self.addDomain = QtWidgets.QPushButton(self.domainList)
        self.addDomain.setGeometry(QtCore.QRect(290, 30, 100, 25))
        self.addDomain.setObjectName("addDomain")
        
        self.syncList = QtWidgets.QPushButton(self.domainList)
        self.syncList.setGeometry(QtCore.QRect(290, 110, 100, 25))
        self.syncList.setObjectName("syncList")
        
        self.tabWidget.addTab(self.domainList, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
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
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Wordpress Vunerabiltiy Scanner"))
        self.initiateManualScan.setText(_translate("MainWindow", "SCAN"))
        self.automationEnable.setText(_translate("MainWindow", "Automate?"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.scanTab), _translate("MainWindow", "Scan"))
        self.domainInput.setText(_translate("MainWindow", "www.wordpressite.com"))
        self.label.setText(_translate("MainWindow", "Add Domain"))
        self.addDomain.setText(_translate("MainWindow", "Add domain"))
        self.syncList.setText(_translate("MainWindow", "Sync List"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.domainList), _translate("MainWindow", "Domains"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Schedule"))
        self.menuWordPress_Scan.setTitle(_translate("MainWindow", "WordPress Scanner"))


if __name__ == '__main__':
    window = Ui_MainWindow()
    Ui_MainWindow.setupUi
