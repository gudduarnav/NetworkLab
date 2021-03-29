# broadcast to all address in the subnet
# ipv4 broadcast address is X.Y.Z.255
# ipv6 broadcase address ::

try:
    from twisted.internet.protocol import DatagramProtocol
    from twisted.internet import reactor
except ImportError as __ex:
    print("Install twisted. Exception:", str(__ex))
    exit(1)

from socket import SOL_SOCKET, SO_BROADCAST


class Echo(DatagramProtocol):
    def startProtocol(self):
        self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        self.transport.write(b'Hello', ('255.255.255.255', 1001))

    def datagramReceived(self, datagram, addr):
        print("{} sent me: {!r}".format(addr, datagram))
        #self.transport.write(datagram, addr)
        reactor.stop()


def main():
    # port=0 means any port
    reactor.listenUDP(2002, Echo()) # <-- broadcast receiver port
    reactor.run()


if __name__ == "__main__":
    main()

