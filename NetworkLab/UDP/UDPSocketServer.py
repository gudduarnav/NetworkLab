# Pass a nonblocking custom socket to datagram
# Since, we are passing a custom socket, we must clean it

import socket
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
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.setblocking(False)
    s.bind(("0.0.0.0", port))

    port = reactor.adoptDatagramPort(s.fileno(), socket.AF_INET, Echo())

    s.close()
    reactor.run()

if __name__ == "__main__":
    main()


