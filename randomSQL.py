import sqlite3
sqlConnection = sqlite3.connect("battleships.db")
sqlStatement = "DELETE FROM Player"
sqlConnection.execute(sqlStatement)
sqlConnection.commit()

