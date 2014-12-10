# CIS 467 Capstone Project - Cafe Messenger
#
# This will be the container for the main prototype window.
# It will simply feature a friend's list on the right side,
# and the chat window on the left side. I'm considering
# having every friend opened to have its own independent
# frame, but that may be implemented later in the long run.
#
#
#
#
#
from twisted.internet import reactor
from CafeAddFriendFrame import AddFriend
from CafeChatPanel import ChatPanel
from CafeFriendPanel import FriendPanel
from CafeMainMenuBar import MainMenu
import Tkinter as tk
import cPickle as pickle
import crypto.crypto_controller as crypto

import random

HOST = ''
PORT = 1025


class MainFrame(tk.Tk):

    """
    """

    def create_panels(self):
        """
        """
        self.container_frame.config(width=800, height=630)
        self.container_frame.place(x=0, y=0, anchor="nw")

        # Display the menu
        self.config(menu=self.menubar)

        # Create and place the Friends List
        self.friends.config(width=190, height=590)
        self.friends.place(x=5, y=5, anchor="nw")

    def quit(self):
        """
        """
        reactor.stop()

    def add_friend(self):
        """
        """
        t = AddFriend(self, crypto.get_public_key_string(self.myKeys))
        t.grab_set()
        self.flist = crypto.get_friend_list(self.name)

    def confirm_friend(self, info):
        """
        """
        try:
            if crypto.add_friend(self.name, info["name"], info["key"]):
                self.friends.add_friend(info["name"])
                self.conn[info["name"]] = (None, -1)
                self.print_connections()
                return 0
            else:
                return 1
        except:
            return -1

    def remove_friend(self, name):
        """
        """
        if not crypto.delete_friend(self.name, name):
            print "Something went wrong with crypto.delete_friend."
            print "Consider reloading the client to get correct friend list."
        else:
            del self.conn[name]
            self.print_connections()

    def send_auth_packet(self, convo_id, sym_key, friend_RSA):
        """
        """
        packet = crypto.gen_packet_a("A",
                                     "Source",
                                     "Destination",
                                     convo_id,
                                     sym_key,
                                     friend_RSA,
                                     self.myKeys)
        self.write_to_transport(packet)
        print "Sending A packet!"

    def window_closed(self, convo_id, sym_key, friend_convo_id):
        """
        """
        packet = crypto.gen_packet_s("C", "Source", "Destination",
                                     friend_convo_id,
                                     "close " + str(convo_id),
                                     sym_key,
                                     self.myKeys)
        for i in self.conn:
            if self.conn[i][1] is convo_id:
                self.conn[i] = (None, -1)
        self.write_to_transport(packet)
        print "Sent C(close) packet."

    def handle_packet(self, packet):
        """
        """
        print "Got a packet to handle!"
        p_type = crypto.json_get_packet_type(packet)
        c_id = int(crypto.json_get_convo_id(packet))
        print c_id

        if p_type == "M":
            print "M Type Packet received."
            t = self.winlist[c_id]
            sym_key = t.get_sym_key()
            friend = t.get_name()
            friend_RSA = crypto.load_friend(self.name, friend)
            decrypted_packet_m = crypto.decrypt_packet_s(packet, sym_key,
                                                         friend_RSA)
            if decrypted_packet_m is not False:
                message = decrypted_packet_m.get_data()
                self.append_message(friend, message[:-1], c_id)
            else:
                print "Signature does not match key, tossing packet!"
                return 'break'

        if p_type == "C":
            print "C Type Packet received."
            t = self.winlist[c_id]
            sym_key = t.get_sym_key()
            friend = t.get_name()
            friend_RSA = crypto.load_friend(self.name, friend)
            decrypted_packet_c = crypto.decrypt_packet_s(packet, sym_key,
                                                         friend_RSA)
            if decrypted_packet_c is not False:
                command = decrypted_packet_c.get_data().split(" ")
                if command[0] == "accept":
                    t.set_friend_convo_id(int(command[1]))
                    print "Accept Command packet received, ready for chat."
                    return 'break'

                if command[0] == "close":
                    print "Client closed window, commence closing ours."
                    t.destroy()
                    return 'break'
                """
                if command[0] == "future_command":
                    print "This is a blank space for a potentially new command"
                    return 'break'
                """
                print "Unknown command type. Packet thrown."
                return 'break'

            else:
                print "Signature does not match key, tossing packet!"
                return 'break'

        if p_type == "A":
            print "A Type Packet received."
            d_packet_a = crypto.decrypt_packet_a(packet, self.myKeys)
            public_key = d_packet_a.get_sender_key()
            for i in self.flist:
                friend_name = i[:-4]
                # Load a friend from our friends list.
                friend_RSA = crypto.load_friend(self.name, friend_name)
                # Does this packet come from a user in our friends list?
                if public_key == crypto.get_public_key_string(friend_RSA):
                    # Verify the integrity of the packet using its signature.
                    if crypto.verify_packet(packet, friend_RSA):
                        number = self.recv_chat(friend_name,
                                                d_packet_a.get_convo_id(),
                                                d_packet_a.get_data())
                        packet = crypto.gen_packet_s("C", "Source",
                                                     "Destination",
                                                     d_packet_a.get_convo_id(),
                                                     "accept " + str(number),
                                                     d_packet_a.get_data(),
                                                     self.myKeys)
                        self.write_to_transport(packet)
                        print "Sending C(accept) packet!"
                        return 'break'
                    # The packet was corrupted or signed by a stranger.
                    else:
                        print "Signature does not match key, tossing packet!"
                        return 'break'

            print "Not a friend! (tossed)"
            return 'break'



    def send_chat(self, name):
        # Are we already chatting with that user?
        for i in self.conn:
            if i == name:
                if not self.conn[i][1] == -1:
                    print "Already chatting with that user!"
                    return 'break'
        
        # New chat session!
        print "Chat Start!"
        sym_key = crypto.generate_symmetric_key()
        convo_id = self.generate_convo_id()
        t = ChatPanel(self, self.name, name, convo_id,
                      None, sym_key)
        self.winlist[convo_id] = t
        reactor.connectTCP(self.conn[name][0][0], 
                           self.conn[name][0][1], 
                           GreeterFactory())
        self.conn[name] = (self.conn[name][0], convo_id)
        
        friend_RSA = crypto.load_friend(self.name, name)
        self.send_auth_packet(convo_id, sym_key, friend_RSA)

    def recv_chat(self, name, their_number, proposed_key):
        print "Chat received!"
        convo_id = self.generate_convo_id()
        t = ChatPanel(self, self.name, name, convo_id,
                      their_number, proposed_key)
        self.winlist[convo_id] = t
        reactor.connectTCP(self.conn[name][0][0], 
                           self.conn[name][0][1], 
                           GreeterFactory())
        self.conn[name] = (self.conn[name][0], convo_id)
        return convo_id

    def generate_convo_id(self):
        """
        """
        """
        number = -1
        while number < 10000:
            number = number + 1
            try:
                self.winlist[number]
            except KeyError:
                return number

        print "Number Exceeded, abort."
        return -1
        """
        flag = True
        while flag:
            number = random.randrange(10000)
            try:
                self.winlist[number]
            except KeyError:
                return number
        

    def append_message(self, name, message, convo_id):
        """This method sends a message and name to the chat panel.

        Invokes the text_area_append method of the ChatPanel class.
        It sends a name and a message to be appended on the textarea.

        """
        try:
            self.winlist[convo_id].text_area_append(name, message)
        except IndexError:
            print "Another friend is trying to reach the client."
            return 'break'
        except:
            print "Window is gone and the other client failed to close his."
            """
            packet = crypto.gen_packet_s("C", "Source", "Destination",
                                         convo_id,
                                         "newinstance",
                                         d_packet_a.get_data(),
                                         self.myKeys)
            packet_pickle = pickle.dumps(packet)
            self.write_to_transport(packet_pickle)
            print "Sending C(resend) packet!"
            """
            return 'break'

    def change_chat_name(self, name):
        """This method sends a name to the chat panel to be changed.

        Invokes the change_chat_name method of the ChatPanel class.

        """
        self.chat.change_chat_name(name)

    def send(self, message, convo_id, sym_key):
        """This method receives a message from its chat child and forwards it.

        This is a callback chain specific method. It will receive a message
        from the child, then forward that message to the controller which
        will have a method called "send_message(message)"

        Args:
        message: The message that will be sent to the controller.

        """

        packet = crypto.gen_packet_s("M", "Source", "Destination", convo_id,
                                     message, sym_key, self.myKeys)
        self.write_to_transport(packet)
        print "Sending M packet!"

    def write_to_transport(self, packet):
        """
        """
        print "For now no connections are made. Instead print out conn table!"
        self.print_connections()
        # self.conn.transport.write(packet)

    def populate_connections_list(self):
        """
        """
        
        def friend_ip_connector(info):
            print "THIS IS THE STUFF---------------------"
            print info.result
            info = info.result[1:-1]
            info = info.split(",")
            self.conn[friend_name] = (info, -1)
        
        for i in self.flist:
            friend_name = i[:-4]
            RSA_friend = crypto.load_friend(self.name, friend_name)
            publickey = crypto.get_public_key_string(RSA_friend)
            info = self.dhtServer.get(publickey)
            info.addCallback(friend_ip_connector)

    def print_connections(self):
        """
        """
        for i in self.conn:
            print i + " " + str(self.conn[i][1])
        print ""

    def __init__(self, dhtServer, conn, myKeys, name, *args, **kwargs):
        """
        """
        self.name = name
        self.myKeys = myKeys
        self.conn = conn
        print "\nWelcome to CAFE Messenger! (debug mode)\n"
        tk.Tk.__init__(self, *args, **kwargs)
        self.chatCount = 0
        self.winlist = {}
        self.dhtServer = dhtServer
        self.container_frame = tk.Frame(self)
        self.menubar = MainMenu(self)
        self.flist = crypto.get_friend_list(self.name)
        self.populate_connections_list()
        self.print_connections()
        self.friends = FriendPanel(self, self.name, self.flist)

        self.title("Cafe")
        self.maxsize(200, 630)
        self.minsize(200, 630)

        self.protocol('WM_DELETE_WINDOW', self.quit)
        self.create_panels()
