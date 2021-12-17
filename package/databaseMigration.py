from os import close
from posixpath import defpath
from PyQt5.QtSql import *
import os.path


def databaseCheck():
    
    #domains = []

    
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("wpscanDomainList.db")
    db.open()
    createTable = QSqlQuery()
    createTable.exec( # Creates database to store domain names
        """
        CREATE TABLE domains (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            monday VARCHAR(100) UNIQUE NOT NULL,
            tuesday VARCHAR(100) UNIQUE NOT NULL,
            wednesday VARCHAR(100) UNIQUE NOT NULL,
            thursday VARCHAR(100) UNIQUE NOT NULL,
            friday VARCHAR(100) UNIQUE NOT NULL
        )
        """
    )
    
    #with open('domains/domains.txt') as d:
     #       domains = d.readlines()

    #for line in domains: # inputs into database already existing domains in txt file
    #    inputDomainQuery = QSqlQuery()
#
    #    inputDomainQuery.prepare(
    #        """
    #        INSERT INTO domains (
    #            domain
    #        )
    #        VALUES (?)
    #        """
    #    )
    #    inputDomainQuery.addBindValue(line)
    #    inputDomainQuery.exec()

   
    
    return None
    

