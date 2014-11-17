# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CIS 467 Capstone Project - Cafe Messenger
# CafeGUIController.py
# Authors: Michael Currie & Mark Aiken
#
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import socket
import time

from twisted.internet import tksupport, reactor, protocol, endpoints
from twisted.internet.protocol import ClientFactory
from twisted.protocols import basic

from CafeLoginFrame import LoginFrame
from CafeMainFrame import MainFrame
import cPickle as pickle


HOST1 = '35.40.217.203'
HOST2 = '35.40.139.16'
PORT = 1025


class RSAObject():

    def amend(self, RSAObject, name):
        self.Object = RSAObject
        self.name = name

    def get(self):
        return self.Object

    def get_name(self):
        return self.name

    def __init__(self):
        self.Object = None
        self.name = None


class Greeter(basic.LineReceiver):

    """
    This class is the listener for the twisted framework. All incoming messages
    will route through here in the lineReceived function.
    """

    def lineReceived(self, this_pickle):
        print "Line has been received!"
        packet = pickle.loads(this_pickle)
        top.handle_packet(packet)

        """
        print "Incoming:\n" + line
        key = b'01234567890123450123456789012345'
        pmsg = crypto.decrypt_message(key, line)
        print "Decrypted:\n" + pmsg + "\n"
        top.append_message("Server_Echo", pmsg)
        """

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

if __name__ == "__main__":
    print socket.gethostname()
    host = socket.gethostbyname(socket.gethostname())
    print host
    print "Accepted IP's: " + HOST1 + " or " + HOST2
    if host == HOST1:
        friend = HOST2
        print "Welcome! This program will attempt to connect to " + friend
    else:
        if host == HOST2:
            friend = HOST1
            print "Welcome! This program will attempt to connect to " + friend
        else:
            print "This is not a usable computer for testing."
            print "Please change the predetermined ip addresses at the top."
            quit()
    this = RSAObject()
    top = LoginFrame(this)
    top.mainloop()
    if this.get() is None:
        quit()

    factory = GreeterFactory()
    connPort = PORT
    routerNode = False

    """
    # Setup intial routing node
    if (not os.path.isfile('tmpFile')):
        routerNode = True
        ser = endpoints.serverFromString(reactor, "tcp:0").listen(
            PubFactory()).result
        #  TODO Error Handling
        f = open('tmpFile', 'w')
        f.write(str(ser.getHost().port))
        f.close()

    # Connect to existing routing node
    f = open('tmpFile', 'r')
    connPort = int(f.readline())
    f.close()
    # TODO Error handling
    """

    reactor.listenTCP(PORT, GreeterFactory())
    conn = reactor.connectTCP(friend, PORT, GreeterFactory())
    top = MainFrame(None, conn, this.get(), this.get_name())
    tksupport.install(top)
    reactor.run()
    if routerNode:
        os.remove('tmpFile')
