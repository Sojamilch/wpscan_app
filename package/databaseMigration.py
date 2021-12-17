from os import close
from posixpath import defpath
from PyQt5.QtSql import *
import os.path

class databaseControlling():

    def databaseCheck(self):
        
       

        
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("wpscanDomainList.db")
        db.open()
        createTable = QSqlQuery()
        createTable.exec( # Creates database to store domain names
            """
            CREATE TABLE domains (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                monday VARCHAR(100) UNIQUE,
                tuesday VARCHAR(100) UNIQUE,
                wednesday VARCHAR(100) UNIQUE,
                thursday VARCHAR(100) UNIQUE,
                friday VARCHAR(100) UNIQUE 
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
        return print(db.tables())

    def inputDomain(self, day, value):

        inputDomainQuery = QSqlQuery()

        if day == "Monday":
            inputDomainQuery.prepare(
            """
            INSERT INTO domains (
                monday
            )
            VALUES ( ? )
            """
            )
        elif day == "Tuesday":
            inputDomainQuery.prepare(
            """
            INSERT INTO domains (
                tuesday
            )
            VALUES ( ? )
            """
            )
        elif day == "Wednesday":
            inputDomainQuery.prepare(
            """
            INSERT INTO domains (
                wednesday
            )
            VALUES ( ? )
            """
            )
        elif day == "Thursday":
            inputDomainQuery.prepare(
            """
            INSERT INTO domains (
                thursday
            )
            VALUES ( ? )
            """
            )
        elif day == "Friday":
            inputDomainQuery.prepare(
            """
            INSERT INTO domains (
                friday
            )
            VALUES ( ? )
            """
            )
    
        inputDomainQuery.addBindValue(value)
        inputDomainQuery.exec()
        
    

