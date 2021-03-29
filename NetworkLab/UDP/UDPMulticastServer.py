# Multicast: Send to multiple host with a single server

try:
    from twisted.internet.protocol import DatagramProtocol
    from twisted.internet import reactor
except ImportError as __ex:
    print("Install twisted. Exception:", str(__ex))
    exit(1)

class MulticastPingPong(DatagramProtocol):
    def startProtocol(self):
        # for TTL>1 allows hopping through multiple routers
        self.transport.setTTL(5)

        # join  a specific multicast group
        self.transport.joinGroup("224.0.0.0")

    def datagramReceived(self, datagram, addr):
        print("Datagram received from {}: {}".format(repr(addr), repr(datagram)))

        if datagram == b"Client: Ping" or datagram == "Client: Ping":
            # rather than sending reply to all, send reply to the sender
            self.transport.write(b"Server: Pong", addr)
            print("Server replied Server: Pong to client {}".format(repr(addr)))

def main():
    reactor.listenMulticast(1001, MulticastPingPong(), listenMultiple=True)
    reactor.run()

if __name__ == "__main__":
    main()



