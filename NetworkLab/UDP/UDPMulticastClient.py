try:
    from twisted.internet.protocol import DatagramProtocol
    from twisted.internet import reactor
except ImportError as __ex:
    print("Install twisted. Exception:", str(__ex))
    exit(1)
    
class MulticastPingClient(DatagramProtocol):
    def startProtocol(self):
        self.transport.setTTL(5)

        # join the multicast group
        self.transport.joinGroup("224.0.0.0")

        # send data to multicast group
        self.transport.write(b"Client: Ping", ("224.0.0.0", 1001)) # write to multicast port

    def datagramReceived(self, datagram, addr):
        print("Reply from {}: {}".format(repr(addr), repr(datagram)))


def main():
    # listen for reply on different unicast port
    reactor.listenMulticast(9999, MulticastPingClient(), listenMultiple = True)
    reactor.run()


if __name__ == "__main__":
    main()


