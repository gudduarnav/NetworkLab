# connected udp means that it is connected to a single client for send/receive use

try:
    from twisted.internet.protocol import DatagramProtocol
    from twisted.internet import reactor
except ImportError as __ex:
    print("Install twisted. Exception:", str(__ex))
    exit(1)


class Hello(DatagramProtocol):
    def startProtocol(self):
        host = "127.0.0.1"
        port = 1001

        self.transport.connect(host, port)
        print("we are connected to", (host, port))
        self.transport.write(b"Hello")

    def datagramReceived(self, datagram, addr):
        print("received from {}: {!r}".format(addr, datagram))
        self.transport.write(datagram)

    def connectionRefused(self):
        print("ERROR: No one is listening")


def main():
    reactor.listenUDP(0, Hello())
    reactor.run()

if __name__ == "__main__":
    main()


