try:
    from twisted.internet import protocol, reactor
except ImportError as ex:
    print("Install twisted. Exception:", str(ex))

import datetime

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        print("Connected to Server")
        s = "Current Time is {}".format(datetime.datetime.now())
        self.transport.write(s.encode("UTF-8"))

    def dataReceived(self, data):
        print("Server said", data.decode("UTF-8"))
        self.transport.loseConnection()

    def connectionLost(self, reason):
        print("Disconnected from Server")


class ProtocolFactory(protocol.ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print("Connection Failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection Lost")
        reactor.stop()

def main():
    f = ProtocolFactory()
    host = "127.0.0.1"
    port = 5555
    reactor.connectTCP(host, port, f)
    reactor.run()


if __name__=="__main__":
    main()