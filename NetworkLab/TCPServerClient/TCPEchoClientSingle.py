# Single client based TCP Client

import socket
from datetime import datetime

class Client:
    def __init__(self,
                 host="127.0.0.1",
                 port=5555):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        print("Connected to", (host, port))


    def writedata(self, data:str):
        bytedata = data.encode("UTF-8")
        self.s.send(bytedata)

    def readdata(self, n=1024):
        bytedata = self.s.recv(n)
        return bytedata.decode("UTF-8")

    def __del__(self):
        self.s.close()
        print("Connection closed")


def main():
    c = Client()

    while True:
        c.writedata(str(datetime.now())+"\n")
        print(c.readdata())

        choice = input("Try again (Y/N)?").strip()
        if "n" in choice.lower():
            print("Exiting...")
            break




if __name__=="__main__":
    main()


