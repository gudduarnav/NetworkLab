try:
    from twisted.internet.protocol import DatagramProtocol
    from twisted.internet import reactor
except ImportError as __ex:
    print("Install twisted. Exception:", str(__ex))
    exit(1)


class Echo(DatagramProtocol):
    def datagramReceived(self, datagram, addr):
        print("{} sent: {!r}".format(addr, datagram))
        self.transport.write(datagram, addr)


def main():
    port = 1001
    reactor.listenUDP(port, Echo())
    reactor.run()

if __name__ == "__main__":
    main()


