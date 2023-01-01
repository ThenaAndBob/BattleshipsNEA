import sqlite3
sqlConnection = sqlite3.connect("battleships.db")
sqlStatement = "DELETE FROM Game"
sqlConnection.execute(sqlStatement)
sqlConnection.commit()