import sqlite3
# sqlConnection = sqlite3.connect("battleships.db")
# sqlStatement = "DELETE FROM Player"
# sqlConnection.execute(sqlStatement)
# sqlConnection.commit()

sqlConnection = sqlite3.connect("battleships.db")
sqlStatement = "SELECT MAX(gameID) FROM Game"
result = sqlConnection.execute(sqlStatement).fetchone()[0]
print(result)