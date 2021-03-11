# Echo server using Twisted
try:
    from twisted.internet import protocol, reactor
except ImportError as ex:
    print("Install twisted. Exception:", str(ex))
    exit(1)


class EchoProtocol(protocol.Protocol):
    def __init__(self):
        self.peer = None

    def connectionMade(self):
        self.peer = self.transport.getPeer()
        print("Client connected from", str(self.peer))

    def dataReceived(self, data):
        s = data.decode("UTF-8")
        print("Client", self.peer.host, self.peer.port,"said", s)
        databytes = s.encode("UTF-8")
        self.transport.write(databytes)

    def connectionLost(self, reason):
        print("Client", self.peer.host, self.peer.port,"disconnected")


class ProtocolFactory(protocol.ServerFactory):
    protocol = EchoProtocol


def main():
    factory = ProtocolFactory()
    port = 5555
    reactor.listenTCP(port, factory)
    print("Listening for client on port", port, "...")
    reactor.run()

if __name__=="__main__":
    main()

