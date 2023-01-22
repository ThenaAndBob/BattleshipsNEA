import socket

#########################################################################
#
# CATEGORY A SKILL: Client-server model
# The network class acts as a middle man between the UI and server.
#
#########################################################################
class Network():
    def __init__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._serverIP = "192.168.2.49" #"172.16.2.150" 
        self._port = 5555
        self._mySocket = (self._serverIP, self._port)
        self._id = self.connect()

    def connect(self):
        self._client.connect(self._mySocket)
        return self._client.recv(2048).decode()

    def send(self, data):
        try:
            self._client.send(str.encode(data))
            return self._client.recv(2048).decode()
        except socket.error as e:
            print(e)
