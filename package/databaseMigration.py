from posixpath import defpath
from PyQt5.QtSql import *
import os.path


def databaseCheck():
    
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("wpscanDomainList.db")
    db.open()
    createTable = QSqlQuery()
    createTable.exec( # Creates database to store domain names
        """
        CREATE TABLE domains (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            domain VARCHAR(100) UNIQUE NOT NULL
        )
        """
    )
    
    return print(db.tables())
    

