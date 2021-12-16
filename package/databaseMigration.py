from PyQt5.QtSql import *

db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("wpscanDomainList.db")
db.open()
createTable = QSqlQuery()
createTable.exec(
    """
    CREATE TABLE domains (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        domain VARCHAR(100) NOT NULL
    )
    """
)

print(db.tables())