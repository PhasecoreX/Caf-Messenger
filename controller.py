# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CIS 467 Capstone Project - Cafe Messenger
# CafeGUIController.py
# Authors: Michael Currie & Mark Aiken
#
#   Requires:
#   twisted
#   PyCrypto
#   idlib
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from kademlia.network import Server
from twisted.internet import tksupport, reactor, protocol
from twisted.internet.protocol import ClientFactory
from twisted.protocols import basic
from twisted.python import log
import argparse
import ipgetter
import socket
import sys
import time

from gui.CafeLoginFrame import LoginFrame
from gui.CafeMainFrame import MainFrame
import crypto.crypto_controller as crypto_controller
log.startLogging(sys.stdout)

parser = argparse.ArgumentParser(description="Python Chat, sunny side up.")
parser.add_argument('--bootstrap', dest='bootUrlIp',
                    default='hook.do.royalaid.me', type=str,
                    help='The url or IP used to bootstrap this node')

args = parser.parse_args()

PORT = 1025
DHTPORT = 2233
THISIP = ipgetter.myip()
BOOTURL = args.bootUrlIp
publicKey = None


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


def bootstrapDone(top, server, rsaObj):
    print "Key insterting"
    server.set(publicKey, "(" + THISIP + ',' + str(PORT) + ")")
    print "Key set"
    conn = {}
    top = MainFrame()
    top.start(server, conn, rsaObj.get(), rsaObj.get_name())
    tksupport.install(top)


if __name__ == "__main__":
    dhtServer = Server()
    if socket.gethostbyname(BOOTURL) == THISIP:
        dhtServer.listen(DHTPORT)
        dhtServer.bootstrap([('127.0.0.1', DHTPORT)])
    else:
        dhtServer.listen(DHTPORT + 10)
        rsaObj = RSAObject()
        top = LoginFrame(rsaObj)
        top.mainloop()
        if rsaObj.get() is None:
            quit()
        bootip = socket.gethostbyname(BOOTURL)
        publicKey = crypto_controller.get_public_key_string(rsaObj.get())
        top = dhtServer.bootstrap([(bootip, DHTPORT)]).addCallback(bootstrapDone,
                                                                   dhtServer,
                                                                   rsaObj)
        print "THIS IS IMPORT YO" + str(top)
        factory = GreeterFactory()
        connPort = PORT
        tmpReactor = reactor.listenTCP(PORT, GreeterFactory())
        print THISIP + ': ' + str(PORT)
        if socket.gethostbyname(BOOTURL):
            print socket.gethostbyname(BOOTURL)

    reactor.run()
