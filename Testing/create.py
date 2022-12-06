import sqlite3

conn = sqlite3.connect('test.db')

print("Opened database successfully")

stmt = """CREATE TABLE COMPANY
        (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         AGE            INT     NOT NULL,
         ADDRESS        CHAR(50),
         SALARY         REAL);"""

conn.execute(stmt)

print("Table created successfully")

conn.close()
