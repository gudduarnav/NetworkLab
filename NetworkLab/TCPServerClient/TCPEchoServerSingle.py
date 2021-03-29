# Single client based TCP Server

import socket

class Server:
    def __init__(self,
                 host="0.0.0.0",
                 port=5555):
        print("Create socket...")
        self.s = socket.socket(socket.AF_INET,
                               socket.SOCK_STREAM)

        print("Bind to", (host, port))
        self.s.bind((host, port))

        print("Listen for client connection")
        self.s.listen()

    def acceptclient(self):
        (self.client, self.clientaddr) = self.s.accept()
        print("Client connected from", self.clientaddr)

    def readClientData(self, n=1024):
        bytedata= self.client.recv(n)
        if not bytedata:
            return None

        return bytedata.decode("UTF-8")

    def writeClientData(self, data:str):
        bytedata = data.encode("UTF-8")
        self.client.send(bytedata)


    def closeclient(self):
        self.client.close()
        print("Client at", self.clientaddr, "closed")

    def __del__(self):
        print("Close server socket")
        self.s.close()
        print("Socket closed")


def main():
    server = Server()
    server.acceptclient()

    while True:
        data = server.readClientData()
        if not data:
            server.closeclient()
            print("Client disconnected")
            break

        server.writeClientData(data)
        print("Client sent", data)





if __name__ == "__main__":
    main()
