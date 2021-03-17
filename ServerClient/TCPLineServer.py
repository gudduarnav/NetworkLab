try:
    from twisted.internet.protocol import Factory
    from twisted.protocols.basic import LineReceiver
    from twisted.internet import reactor
except ImportError as ex:
    print("Install twisted. Exception:", str(ex))


def tobytes(s:str):
    return s.encode("UTF-8")


class LineClient(LineReceiver):
    def connectionMade(self):
        print("client connected from", str(self.transport.getPeer()))
        self.onInit()

    def connectionLost(self, reason):
        print("client", str(self.transport.getPeer()), "disconnected")


    def lineReceived(self, line):
        s_line = line.decode("UTF-8")
        if self.state == "GETNAME":
            self.onName(s_line)
        elif self.state == "GETPLACE":
            self.onPlace(s_line)
        elif self.state == "GETSTAYDURATION":
            self.onStayDuration(s_line)

    def onInit(self):
        self.sendLine(tobytes("What is your Name?"))

        self.name = ""
        self.place = ""
        self.stayduration = 0
        self.state = "GETNAME"

    def onName(self, line):
        self.name = line
        self.sendLine(tobytes("Where are you from?"))
        self.state = "GETPLACE"

    def onPlace(self, line):
        self.place = line
        self.sendLine(tobytes("How long (in years) are you living there?"))
        self.state = "GETSTAYDURATION"

    def onStayDuration(self, line):
        try:
            self.stayduration = int(line)
        except:
            pass

        # process and notify
        response = "Hello, {} from {} place. You are staying at {} for {} years.".format(self.name,
                                                                                         self.place,
                                                                                         self.place,
                                                                                         self.stayduration)
        self.sendLine(tobytes(""))
        self.sendLine(tobytes(response))

        notify = "{} is staying at {} for {} years".format(self.name,
                                                           self.place,
                                                           self.stayduration)
        print(notify)

        # repeat
        self.onInit()

class ProtocolFactory(Factory):
    def __init__(self):
        pass

    def buildProtocol(self, addr):
        return LineClient()




def main():
    reactor.listenTCP(5555, ProtocolFactory())
    reactor.run()

if __name__ == "__main__":
    main()