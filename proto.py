
class Greeter(basic.LineReceiver):

    """
    This class is the listener for the twisted framework. All incoming messages
    will route through here in the lineReceived function.
    """

    def dataReceived(self, packet):
        top.handle_packet(packet)

    def lineReceived(self, packet):
        top.handle_packet(packet)

    def connectionMade(self):
        print "Connection made to friend!\n"

    def connectionLost(self, reason):
        print "Connection Lost!"


class GreeterFactory(ClientFactory):

    def buildProtocol(self, addr):
        return Greeter()

    def clientConnectionLost(self, connector, reason):
        print reason
        print "Connection lost, attempting reconnection . . ."
        time.sleep(3)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print reason
        print "Failed to connect, attempting reconnection . . ."
        time.sleep(3)
        connector.connect()


class PubProtocol(basic.LineReceiver):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.add(self)
        print 'New Connection Established\n'

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print 'Connection Lost\n'

    def lineReceived(self, line):
        line = line + "\r\n"
        print "New Message:\n" + repr(line) + "\nSending Echo...\n"
        for c in self.factory.clients:
            c.transport.write(line)


class PubFactory(protocol.Factory):

    def __init__(self):
        self.clients = set()

    def buildProtocol(self, addr):
        return PubProtocol(self)
