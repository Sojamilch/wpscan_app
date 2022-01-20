from email import header
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
                                                # borrowed from martin fitzpatrick @ https://www.pythonguis.com/faq/editing-pyqt-tableview/
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index) # allows detection of changes in tableviewdata
            return True
        return False

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            headerLabels = ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Monday', 'Tuesday', 'Wednesday','Thursday','Friday']
            return headerLabels[col]
            #self._data.columns[col]

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable



class DomainInput(): # writes domains into the csv ]

    def input(self, domainName, df):


        def writeToCv():
            df.to_csv("../domains/domains.csv", index=False)
            

        for index in df.index:

            for dayOfMonth in range(0,21):
                

                #print(df.index, dayOfWeek) # DEBUG PURPOSES

                try:
                    nextCell = df.iat[index, dayOfMonth]

                    if nextCell is None or np.isnan(nextCell) or df.isnull(nextCell) or pd.isna(nextCell): #detects if cell is null value/nothing in cell
                        df.iat[index, dayOfMonth] = domainName #replaces said cell with input domain
                        writeToCv() # saves cv
                        print(df)
                        return df
                except: 
                    #print(nextCell, "Is not null/nan") DEBUG PURPOSES
                    if nextCell == df.iat[-1,-1]: # if at last value of dataframe add new line to end of dataframe 
                        print("adding new empty line")
                        df = df.append(pd.Series(), ignore_index=True)
                        writeToCv()
        
        return df

                

        
                

        
