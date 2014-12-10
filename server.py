from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic


class PubProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.clients = {}
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.add(self)
        print 'New Connection Established\n'

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print 'Connection Lost\n'

    def lineReceived(self, line):
        print "New Message:\n" + repr(line) + "\nSending Echo...\n"
        for c in self.factory.clients:
            c.transport.write(line)

class PubFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()

    def buildProtocol(self, addr):
        return PubProtocol(self)

endpoints.serverFromString(reactor, "tcp:1025").listen(PubFactory())
reactor.run()
