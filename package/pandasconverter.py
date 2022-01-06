import os.path
from os import close
from posixpath import defpath
import numpy as np
import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtSql import *


class DomainsTableModel(QAbstractTableModel):
    

  

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
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

    
class DomainInput():

    
    def input(self, dayOfWeek, domainName, df):
        

        
        dayOfWeek = dayOfWeek.lower()


        weekdays = {
            "monday":"0",
            "tuesday":"1",
            "wednesday":"2",
            "thursday":"3",
            "friday":"4"
        }


        dayOfWeekInt = int(weekdays.get(dayOfWeek))

        print(dayOfWeek,dayOfWeekInt, domainName)

        for index in df.index:
            print(index)
            print(df.at[index,0])
            if df.isnull(df.at[index,0]) == True:
                df.loc[index, dayOfWeek] = domainName
                print(df)
                df.to_csv(index=False)
                return None

        
