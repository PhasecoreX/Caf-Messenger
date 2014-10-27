# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CIS 467 Capstone Project - Cafe Messenger
# CafeGUIController.py
# Authors: Michael Currie & Mark Aiken
#
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from CafeMainFrame import MainFrame
from CafeLoginFrame import LoginFrame

from twisted.internet.protocol import ClientFactory
from twisted.internet import tksupport, reactor, protocol, endpoints
from twisted.protocols import basic

import os

import crypto

HOST = ''
PORT = 1025

class RSAObject():
    def amend(self, RSAObject):
        self.Object = RSAObject

    def get(self):
        return self.Object

    def __init__(self):
        self.Object = None



class Greeter(basic.LineReceiver):
    """
    This class is the listener for the twisted framework. All incoming messages
    will route through here in the lineReceived function.
    """
    def lineReceived(self, line):
        print "Incoming:\n" + line
        key = b'01234567890123450123456789012345'
        pmsg = crypto.decrypt_message(key, line)
        print "Decrypted:\n" + pmsg + "\n"
        top.append_message("Server_Echo", pmsg)

    def connectionMade(self):
        print "Connection Made to Server!\n"

    def connectionLost(self, reason):
        print "Connection Lost!"


class GreeterFactory(ClientFactory):
    def buildProtocol(self, addr):
        return Greeter()


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
            # c.transport.write("<{}> {}".format(
                                            #  self.transport.getHost(), line))
            c.transport.write(line)

#  def dataReceived(self, data):
    #    print repr(data)
    #    if data.endswith("\r\n") or data.endswith("\n"):
    #        self.lineReceived(data)


class PubFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()

    def buildProtocol(self, addr):
        return PubProtocol(self)

if __name__ == "__main__":    
    this = RSAObject()
    top = LoginFrame(this)
    top.mainloop()
    if this.get() is None:
        quit()
   
    factory = GreeterFactory()
    connPort = 1025
    routerNode = False

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
    conn = reactor.connectTCP(HOST, connPort, GreeterFactory())
    top = MainFrame(None, conn)
    tksupport.install(top)
    reactor.run()
    if routerNode:
        os.remove('tmpFile')
