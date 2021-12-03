import sys

import PyQt5
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.uic import loadUi
from package.mainUi import Ui_MainWindow

class window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        

##def window(): 
  ##  app = QtWidgets.QApplication(sys.argv)
    ##widget = QtWidgets.QWidget()
    ##textLabel = QtWidgets.QLabel(widget)
    ##textLabel.setText("Test")
    ##widget.setGeometry(100,100,200,50)
    ##textLabel.move(50,20)
    ##widget.setWindowTitle("PythonQTTEST")
    ##widget.show()
    ##sys.exit(app.exec_())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec())