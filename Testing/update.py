import sqlite3

conn = sqlite3.connect('test.db')
print("Opened database successfully")

stmt = "UPDATE COMPANY set SALARY = 25000.00 WHERE ID = 1;"
conn.execute(stmt)

stmt = "UPDATE COMPANY set SALARY = 20000.00 WHERE ID = 2;"
conn.execute(stmt)

conn.commit()

print("Total number of rows updated :", conn.total_changes)
conn.close()
