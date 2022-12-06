import socket

class Network():
    def __init__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server = "192.168.1.238"
        self._port = 5555
        self._mySocket = (self._server, self._port)
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
