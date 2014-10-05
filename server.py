from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
 
 
class PubProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.factory = factory
 
    def connectionMade(self):
        self.factory.clients.add(self)
        self.transport.write("Welcome!\r\n")
        print 'Connection'
 
    def connectionLost(self, reason):
        self.factory.clients.remove(self)
 
    def lineReceived(self, line):
        line = line + "\r\n"
        print repr(line)
        for c in self.factory.clients:
            c.transport.write("<{}> {}".format(self.transport.getHost(), line))


    #def dataReceived(self, data):
    #    print repr(data)
    #    if data.endswith("\r\n") or data.endswith("\n"):
    #        self.lineReceived(data)

 
class PubFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()
 
    def buildProtocol(self, addr):
        return PubProtocol(self)
 
endpoints.serverFromString(reactor, "tcp:1025").listen(PubFactory())
reactor.run()