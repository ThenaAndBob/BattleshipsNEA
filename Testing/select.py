import sqlite3

conn = sqlite3.connect('test.db')
print("Opened database successfully")

stmt = "SELECT id, name, address, salary from COMPANY"
results = conn.execute(stmt)

for row in results:
    id,name,address,salary = row
    print(f"""
ID = {id}
NAME = {name}
ADDRESS = {address}
SALARY = ${salary}
""")

print("Operation done successfully")
conn.close()
