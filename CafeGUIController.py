# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#	CIS 467 Capstone Project - Cafe Messenger
#	CafeGUIController.py
#	Author: Michael Currie
#	
#	
#	
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from CafeMainFrame import MainFrame

from twisted.internet.protocol import ClientFactory
from twisted.internet import tksupport, reactor
from twisted.protocols import basic

import crypto

HOST = ''
PORT = 1025

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


if __name__ == "__main__":
    
    factory = GreeterFactory()
    conn = reactor.connectTCP(HOST, PORT, GreeterFactory())
    top = MainFrame(None, conn)
    
    # top.mainloop()
    tksupport.install(top)
    reactor.run()