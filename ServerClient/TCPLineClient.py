try:
    from twisted.internet.protocol import ClientFactory
    from twisted.protocols.basic import LineReceiver
    from twisted.internet import reactor
except ImportError as ex:
    print("Install twisted. Exception:", str(ex))

def tostring(b:bytes):
    return b.decode("UTF-8")

def tobytes(s:str):
    return s.encode("UTF-8")


class LineClient(LineReceiver):
    def connectionMade(self):
        print("Connection made to Server...")


    def connectionLost(self, reason):
        print("Connection to Server lost")

    def lineReceived(self, line):
        s_line = tostring(line)
        if len(s_line.strip()) < 5 or ("Hello" in s_line):
            print(s_line)
        else:
            s_in = input(s_line)
            b_in = tobytes(s_in)
            self.sendLine(b_in)



class ProtocolClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print("Connecting...")

    def buildProtocol(self, addr):
        print("Connected.")
        return LineClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection to Server failed")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection to Server lost")
        reactor.stop()


def main():
    f = ProtocolClientFactory()
    host = "127.0.0.1"
    port = 5555
    reactor.connectTCP(host, port, f)
    reactor.run()

if __name__ == "__main__":
    main()