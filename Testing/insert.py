import sqlite3

conn = sqlite3.connect('test.db')
print("Opened database successfully")

stmt = """INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
      VALUES (1, 'Paul', 32, 'California', 20000.00 )"""

conn.execute(stmt)

stmt = """INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
      VALUES (2, 'Allen', 25, 'Texas', 15000.00 )"""

conn.execute(stmt)

stmt = """INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) 
      VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )"""

conn.execute(stmt)

stmt = """INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
      VALUES (4, 'Mark', 25, 'Richmond ', 65000.00 )"""

conn.execute(stmt)

conn.commit()
print("Records created successfully")
conn.close()
