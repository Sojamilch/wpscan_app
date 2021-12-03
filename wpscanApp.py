import sys

import PyQt5
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.uic import loadUi
from package.mainUi import Ui_MainWindow

class window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.completed = 0
        
    #//////Testing how to refer to objects and maniplulate////
        self.initiateManualScan.clicked.connect(self.increaseProgress)

    def increaseProgress(self):
        
        self.completed += 1
        self.scanProgressBar.setValue(self.completed)

    #/////////////////////////////////////////////////////////


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec())