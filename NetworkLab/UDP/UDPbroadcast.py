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
from datetime import datetime

class Echo(DatagramProtocol):
    def startProtocol(self):
        self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)

    def datagramReceived(self, datagram, addr):
        print("{} sent me: {!r}".format(addr, datagram))
        s = str(datetime.now()).encode("UTF-8")
        self.transport.write(s, ('255.255.255.255', 2002)) # <= reply on a new broadcast IP and port

def main():
    # port=0 means any port
    reactor.listenUDP(1001, Echo())
    reactor.run()

if __name__ == "__main__":
    main()

