import os.path
from os import close
from posixpath import defpath
import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtSql import *


class DomainsTableModel(QAbstractTableModel): # Generates a model for a tableview 
    

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        
        data.to_csv("./domains/domains.csv", index=False)

        self._data = data
        
    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]
    
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

    def setData(self, index, value, role):

        if not index.isValid():
            return False

        if role != QtCore.Qt.EditRole:
            return False

        row = index.row()

        if row < 0 or row >= len(self._data.values):
            return False

        column = index.column()

        if column < 0 or column >= self._data.columns.size:
            return False

        self._data.values[row][column] = value
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index):
        flags = super(self.__class__,self).flags(index)
        flags |= QtCore.Qt.ItemIsEditable
        flags |= QtCore.Qt.ItemIsSelectable
        flags |= QtCore.Qt.ItemIsEnabled
        return flags
    

class domianEditorDelegate(QtWidgets.QstyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QtWidgets.QComboBox(parent)
        value = index.data()
        options = [value, 'Option 1','Option 2','Option 3','Option 4','Default']
        editor.addItems(options)
        editor.currentTextChanged.connect(self.commitAndCloseEditor)
        return editor

    @QtCore.pyqtSlot()
    def commitAndCloseEditor(self):
        editor = self.sender()
        self.commitData.emit(editor)


class DomainInput():


    # def __init__(self):

    #     df = pd.read_csv("./domains/domains.csv")

    #     df = df.fillna(0)

    #     print(df)

    def input(self, dayOfWeek, domainName, df):
        
        df = df.fillna(' ')

        print(df)

        dayOfWeek = dayOfWeek.lower()


        weekdays = {
            "monday":"0",
            "tuesday":"1",
            "wednesday":"2",
            "thursday":"3",
            "friday":"4"
        }


        dayOfWeekInt = int(weekdays.get(dayOfWeek))

        #print(dayOfWeek,dayOfWeekInt, domainName)

        for index in df.index:
            if df.at[index,dayOfWeek] == ' ':
                df.at[index, dayOfWeek] = domainName
                print(df.at[index, dayOfWeek], "Wrote to CSV!")
                df.to_csv("./domains/domains.csv", index=False)
                return None
            
    
                

        
