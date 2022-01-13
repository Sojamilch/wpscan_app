import os.path
from cmath import isnan
from distutils.fancy_getopt import wrap_text
from os import close
from posixpath import defpath

import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtSql import *


class DomainsTableModel(QAbstractTableModel): # Generates a model for a tableview using pandas dataframes as the data
    

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
        self.dataChanged.emit(index, index) # allows detection of changes in tableviewdata 
        return True

    def flags(self, index):
        flags = super(self.__class__,self).flags(index)
        flags |= QtCore.Qt.ItemIsEditable
        flags |= QtCore.Qt.ItemIsSelectable
        flags |= QtCore.Qt.ItemIsEnabled
        return flags
    



class DomainInput(): # writes domains into the csv ]

    def input(self, domainName, df):


        def writeToCv():
            df.to_csv("../domains/domains.csv", index=False)
            

        

        for index in df.index:

            for dayOfWeek in range(0,5):
                

                #print(df.index, dayOfWeek) # DEBUG PURPOSES

                try:
                    nextCell = df.iat[index, dayOfWeek]

                    if nextCell is None or np.isnan(nextCell) or df.isnull(nextCell) or pd.isna(nextCell): #detects if cell is null value/nothing in cell
                        df.iat[index, dayOfWeek] = domainName #replaces said cell with input domain
                        writeToCv() # saves cv
                        return df
                except: 
                    #print(nextCell, "Is not null/nan") DEBUG PURPOSES
                    if nextCell == df.iat[-1,-1]: # if at last value of dataframe add new line to end of dataframe 
                        print("adding new empty line")
                        df = df.append(pd.Series(), ignore_index=True)
                        writeToCv()

        return df

                

        
                

        
