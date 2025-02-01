import socket
import _thread
import sqlite3
import time

#########################################################################
#
# CATEGORY A SKILL: Client server model and server-side scripting
# Using server-side scripting to query/modify a database and return a result to the user device.
#
#########################################################################
class Server():
    def __init__(self):
        self._games = []
        print("Server started")

    def threading(self, connection):
        connection.send(str.encode("Connected"))
        print("Connected")
        while True: # Continue running while client is connected
            received = connection.recv(2048).decode("utf-8") # receive 2048 bits of data, increase if getting more
            if not received:
                print("No data to receive, disconnecting")
                break
            print("Received:", received)
            data = received.split(" ")
            dataType = data[0]
            
            if dataType.lower() == "signup": 
                print("Signing Up...")
                connection.send(str.encode(self.signUp(data[1], data[2])))
                # signUp returns 'true' or 'false', depending on whether the username can be added to the database.

            elif dataType.lower() == "login":
                print("Logging In...")
                connection.send(str.encode(self.logIn(data[1], data[2])))
            
            elif dataType.lower() == "getloads":
                print("Getting loaded games")
                connection.send(str.encode(self.getLoads(data[1])))

            elif dataType.lower() == "loadgame":
                print("getting grids")
                connection.send(str.encode(self.loadGame(data[1])))

            elif dataType.lower() == "addgame": # Saving a game.
                print("adding game")
                connection.send(str.encode(str(self.addGame(data[1], data[2], data[3], data[4], data[5])))) # g1,g2,u1,u2,prevattack

            elif dataType.lower() == "startgame": # Starting a network game
                print(f"Starting game {data[1]} against {data[2]}")
                connection.send(str.encode(self.startGame(data[1], data[2])))

            elif dataType.lower() == "updategrids":
                print(f"Updating grid of player {data[3]} to {data[1]} in game {data[2]}")
                connection.send(str.encode(self.updateGrids(data[1], data[2], data[3])))

            elif dataType.lower() == "getgrid":
                print(f"Getting grid of player {data[2]} in game {data[1]}")
                connection.send(str.encode(self.getGrid(data[1], data[2]))) # Game id, playernumber

            elif dataType.lower() == "updatepreviousattack":
                print(f"Updating previous attack to type {data[4]} by player {data[3]} at coordinates {data[1]}, {data[2]} in game {data[5]}")
                connection.send(str.encode(self.updatePreviousAttack(data[1], data[2], data[3], data[4], data[5])))

            elif dataType.lower() == "deletegame":
                print(f"Deleting game with game id {data[1]}")
                connection.send(str.encode(self.deleteGame(data[1])))

            elif dataType.lower() == "getstats":
                print(f"Getting stats of player {data[1]}")
                connection.send(str.encode(self.getStats(data[1])))

            elif dataType.lower() == "updatestats":
                print("Updating stats")
                connection.send(str.encode(self.updateStats(data[1], data[2])))

            print("")


        print("Connection lost")
        print("")
        connection.close()

    #########################################################################
    #
    # CATEGORY B SKILL: Single table parameterised SQL and a simple data model in my database.
    # Almost all of the functions after this comment block use SQL to query/modify a databse with
    # a "Players" and "Games" table.
    #
    #########################################################################

    def deleteGame(self,gameID):
        sqlConnection = sqlite3.connect("battleships.db")
        sqlStatement = f"DELETE FROM Game WHERE GameID = '{gameID}'"
        sqlConnection.execute(sqlStatement)
        sqlConnection.commit()
        return "deleted"

    def getStats(self,username):
        sqlConnection = sqlite3.connect("battleships.db")
        sqlStatement = f"SELECT stats FROM Player WHERE username = '{username}'"
        print("Retuning index zero of", sqlConnection.execute(sqlStatement).fetchone())
        return str(sqlConnection.execute(sqlStatement).fetchone()[0])

    def updateStats(self,username,changeStats):
        # wins,losses,hits,misses,highestHP,leastAttacks
        changeStats = list(map(int, changeStats.split(",")))
        currentStats = list(map(int, self.getStats(username).split(",")))
        print(changeStats, currentStats)

        for index, stat in enumerate(changeStats[:4]):
            currentStats[index] += stat
        if currentStats[4] < changeStats[4]:
            currentStats[4] = changeStats[4]
        if currentStats[5] > changeStats[5]:
            currentStats[5] = changeStats[5]

        currentStats = list(map(str, currentStats))
        
        sqlConnection = sqlite3.connect("battleships.db")
        sqlStatement = f"UPDATE Player SET stats = '{','.join(currentStats)}' WHERE username = '{username}'"
        sqlConnection.execute(sqlStatement)
        sqlConnection.commit()
    
        return "updated"

    def signUp(self, username, password):
        sqlConnection = sqlite3.connect("battleships.db")

        print("Creating SQL statement...")
        sqlStatement = f"SELECT username FROM Player WHERE username = '{username}'"

        print("Querying database...")
        result = sqlConnection.execute(sqlStatement)

        if result.fetchone() == None:
            print("Username is unique!")
            sqlStatement = f"INSERT INTO Player (username, password, stats) VALUES ('{username}', '{password}', '0,0,0,0,0,1000000')"
            print(f"Adding username {username} and password {password}...")

            sqlConnection.execute(sqlStatement)
            sqlConnection.commit()
            print("Columns added")

            sqlConnection.close()

            return "unique"

        print("Username was not unique!")
        return "not_unique"

    def logIn(self, username, password):
        sqlConnection = sqlite3.connect("battleships.db")
        sqlStatement = f"SELECT password FROM Player WHERE username = '{username}'"

        result = sqlConnection.execute(sqlStatement)
        storedPass = result.fetchone()
        print(storedPass)

        if not storedPass:
            print(f"Account {username} does not exist")
            return "false"
        elif password == storedPass[0]:
            print("Password was a match!")
        else:
            print("Passwords did not match!")

        return str(password == storedPass[0]).lower()

    def getLoads(self, username): # unsure about return formats
        sqlConnection = sqlite3.connect("battleships.db")
        sqlStatement = f"SELECT gameID FROM Game WHERE username1 = '{username}' OR username2 = '{username}'"
        result = sqlConnection.execute(sqlStatement).fetchall()
        print("Received game IDs - ", result)
        re = ""
        for gameid in result:
            gameid = str(gameid[0])
            print("Game id - ", gameid)
            re += gameid
            re += ","
        re = re[:-1]

        return re

    def loadGame(self, gameID): # unsure about return formats
        sqlConnection = sqlite3.connect("battleships.db")
        sqlStatement = f"SELECT grid1, grid2 FROM Game WHERE gameID = '{gameID}'"
        grids = sqlConnection.execute(sqlStatement).fetchone()
        print("Received grids - ", grids)

        sqlStatement = f"SELECT username2 FROM Game WHERE gameID = '{gameID}'"
        username2 = sqlConnection.execute(sqlStatement).fetchone()[0]
        if username2[:2] == "AI":
            aiLevel = username2[3]
        else:
            aiLevel = "0"

        print("Returning", f"{grids[0]} {grids[1]} {aiLevel}")
        return f"{grids[0]} {grids[1]} {aiLevel}"

    def addGame(self, grid1, grid2, u1, u2, previousAttack):
        sqlConnection = sqlite3.connect("battleships.db")
        sqlStatement = "SELECT MAX(gameID) FROM Game"
        gameID = sqlConnection.execute(sqlStatement).fetchone()[0]
        if gameID is None:
            gameID = 0
        else:
            gameID = int(gameID) + 1
        sqlStatement = f"INSERT INTO Game (gameID, username1, username2, grid1, grid2, previousAttack) VALUES ('{gameID}', '{u1}', '{u2}', '{grid1}', '{grid2}', '{previousAttack}')"
        sqlConnection.execute(sqlStatement)
        sqlConnection.commit()
        return gameID

    def startGame(self, u1, u2):
        if [u2, u1, True, False] in self._games:
            gameIndex = self._games.index([u2, u1, True, False])
            gameID = self.addGame("", "", u2, u1, "")
            self._games[gameIndex] = gameID
            print("Retuning", gameID)
            return f"p2 {gameID}"
        else:
            self._games.append([u1, u2, True, False])
            while not isinstance(self._games[-1], int):
                print("Waiting")
                time.sleep(2)
            print("Player two has connected")
            gameID = self._games[-1]
            self._games.remove(gameID)
            print("Retuning", gameID)
            return f"p1 {gameID}"

    def updateGrids(self, grid, gameID, playerNum):
        sqlConnection = sqlite3.connect("battleships.db")
        sqlStatement = f"UPDATE Game SET grid{int(playerNum)+1} = '{grid}' WHERE gameID = '{gameID}'"
        sqlConnection.execute(sqlStatement)
        sqlConnection.commit()
        return "messageHere"

    def updatePreviousAttack(self, x, y, playerNum, attackType, gameID): # Type: 0 = normal, 1 = barrage, 2 = radar
        playerNum = int(playerNum)
        gameID = int(gameID)
        while True:
            sqlConnection = sqlite3.connect("battleships.db")
            sqlStatement = f"SELECT previousAttack FROM Game WHERE gameID = '{gameID}'"
            previousAttack = sqlConnection.execute(sqlStatement).fetchone()[0] # Get where the enemy attacked last
            print(previousAttack, "", playerNum)
            if previousAttack == "":
                sqlStatement = f"UPDATE Game SET previousAttack = '{x} {y} {attackType} {playerNum}' WHERE gameID = '{gameID}'" 
                sqlConnection.execute(sqlStatement)
                sqlConnection.commit()
                time.sleep(2)
            elif int(previousAttack.split(" ")[3]) == playerNum:
                time.sleep(2) # Wait for player two
                print(f"Waiting for player {(playerNum+1)%2}...")
            else:
                break

        sqlStatement = f"UPDATE Game SET previousAttack = '{x} {y} {attackType} {playerNum}' WHERE gameID = '{gameID}'" 
        sqlConnection.execute(sqlStatement)
        sqlConnection.commit()
        return previousAttack

    def getGrid(self, gameID, playerNum):
        playerNum = int(playerNum)  
        result = ""
        while result is None or result == "":
            sqlConnection = sqlite3.connect("battleships.db")
            sqlStatement = f"SELECT grid{playerNum+1} FROM Game WHERE GameID = '{gameID}'"
            print("Getting grid -", sqlStatement)
            result = sqlConnection.execute(sqlStatement).fetchone()[0]
            time.sleep(2)
        print("Get grid was successful -", result)
        return result

# Server details
serverIP = "192.168.2.49" # "172.16.2.150" 
port = 5555
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
myServer = Server()
mySocket.bind((serverIP, port)) # make the socket (IP + port)

# Connecting to users
numPlayers = 2
mySocket.listen(numPlayers) # listen for 2 devices to connect to server.

while True: # Continually listen for connecting devices
    connection, address = mySocket.accept()  # Accept any connections. 
    # Connection is an object of the connecting device, address is the IP address of that device.
    print("")
    print(f"Connecting to {address} at {time.time()}")

    _thread.start_new_thread(myServer.threading, (connection, )) # Runs function and while loop at the same time. (Multi Threading)
