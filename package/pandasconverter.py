import os.path
from os import close
from posixpath import defpath

import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtSql import *


class DomainsTableModel(QAbstractTableModel):
    

    df = pd.read_csv('./domains/domains.csv')

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





    #def databaseCheck(self): # Commented out for testing purposes (OLD USED FOR SQLite DATABASE HANDLING)
        
       

        
    #     db = QSqlDatabase.addDatabase("QSQLITE")
    #     db.setDatabaseName("wpscanDomainList.db")
    #     db.open()
    #     createTable = QSqlQuery()
    #     createTable.exec( # Creates database to store domain names
    #         """
    #         CREATE TABLE domains (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    #             monday VARCHAR(100) UNIQUE,
    #             tuesday VARCHAR(100) UNIQUE,
    #             wednesday VARCHAR(100) UNIQUE,
    #             thursday VARCHAR(100) UNIQUE,
    #             friday VARCHAR(100) UNIQUE 
    #             )
    #         """
    #     )
        
    #     #with open('domains/domains.txt') as d:
    #     #       domains = d.readlines()

    #     #for line in domains: # inputs into database already existing domains in txt file
    #     #    inputDomainQuery = QSqlQuery()
    # #
    #     #    inputDomainQuery.prepare(
    #     #        """
    #     #        INSERT INTO domains (
    #     #            domain
    #     #        )
    #     #        VALUES (?)
    #     #        """
    #     #    )
    #     #    inputDomainQuery.addBindValue(line)
    #     #    inputDomainQuery.exec()
    #     return print(db.tables())

    # def inputDomain(self, day, value):

    #     inputDomainQuery = QSqlQuery()

    #     if day == "Monday":
    #         inputDomainQuery.prepare(
    #         """
    #         UPDATE domains SET monday = swaws WHERE monday = NULL AND id = 1
            
    #         """
    #         )
    #     elif day == "Tuesday":
    #         inputDomainQuery.prepare(
    #         """
    #         INSERT INTO domains (
    #             tuesday
    #         )
    #         VALUES ( ? )
    #         """
    #         )
    #     elif day == "Wednesday":
    #         inputDomainQuery.prepare(
    #         """
    #         INSERT INTO domains (
    #             wednesday
    #         )
    #         VALUES ( ? )
    #         """
    #         )
    #     elif day == "Thursday":
    #         inputDomainQuery.prepare(
    #         """
    #         INSERT INTO domains (
    #             thursday
    #         )
    #         VALUES ( ? )
    #         """
    #         )
    #     elif day == "Friday":
    #         inputDomainQuery.prepare(
    #         """
    #         INSERT INTO domains (
    #             friday
    #         )
    #         VALUES ( ? )
    #         """
    #         )
    
    #     inputDomainQuery.addBindValue(value)
    #     inputDomainQuery.exec()
        
    

