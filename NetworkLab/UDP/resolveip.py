# resolve ip addresses
try:
    from twisted.internet import reactor
except ImportError as __ex:
    print("Install twisted. Exception:", str(__ex))
    exit(1)

def got_ip(ip):
    print("IP address of localhost is", ip)
    reactor.stop()


def main():
    reactor.resolve("localhost").addCallback(got_ip)
    reactor.run()

if __name__ == "__main__":
    main()

    

