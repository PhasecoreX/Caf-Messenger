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
import sys
import ipgetter
import argparse

from twisted.internet.protocol import ClientFactory
from twisted.internet import tksupport, reactor, protocol, endpoints
from twisted.protocols import basic
from twisted.python import log

import os

from kademlia.network import Server

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

    def dataReceived(self, this_pickle):
        packet = pickle.loads(this_pickle)
        top.handle_packet(packet)

    def lineReceived(self, this_pickle):
        packet = pickle.loads(this_pickle)
        top.handle_packet(packet)

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


def bootstrapDone(found, server):
    server.set("publicKey", "(addr.port)") #TODO Add real vals

if __name__ == "__main__":

    dhtServer = Server()
    if socket.gethostbyname(BOOTURL) == THISIP:
        dhtServer.listen(DHTPORT)
        dhtServer.bootstrap([('127.0.0.1',DHTPORT)])
    else:
        dhtServer.listen(DHTPORT+10)
        bootip = socket.gethostbyname(BOOTURL)
        dhtServer.bootstrap([(bootip, DHTPORT)]).addCallback(bootstrapDone, 
                                                             dhtServer)
        this = RSAObject()
        top = LoginFrame(this)
        top.mainloop()
        if this.get() is None:
            quit()

        factory = GreeterFactory()
        connPort = PORT
        tmpReactor = reactor.listenTCP(PORT, GreeterFactory())
        print THISIP + ': ' + str(PORT)
        if socket.gethostbyname(BOOTURL):
            print socket.gethostbyname(BOOTURL)
        conn = {}
        top = MainFrame(None, conn, this.get(), this.get_name())
        tksupport.install(top)
    reactor.run()
