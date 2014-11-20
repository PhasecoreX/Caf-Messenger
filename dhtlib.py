#####################################################
# A file translating Wikipedia's object oriented    #
# pseudocode into node's viewpoint + packet sending #
# Author: Mark Aiken                                #
# Adapted from http://bit.ly/1uL87Bc                #
#####################################################

def find_successor(node):
    """Finds the successor of node using this node

    :node: The node which has? the successor
    :returns: the succesor of node

    """
    pass

def closest_preceding_node(id):
    """Find the closest preceding node for the given id from the local finger
    table

    :id: The ID to find the closest finger of
    :returns: the node that is closest to the id

    """
    pass

def create_ring():  # Wikiepdia's create
    """Creates a new Chord Ring when one does not exsist

    """
    pass

def ask_join(node):  # Wikipedia's join
    """Asks node for GUID and intial finger table so that this node can join

    :node: The node which we are asking for join information from
    """
    pass

def verify_is_predecessor_of():  # Wikipedia's stablize
    """Asks your immediate successor if you are it's predecessor

    """
    pass

def claim_is_predecessor(node_is_successor):  # Wikipedia's notify
    """Claims that is node is the predecessor of node_is_successor

    :node_is_successor: the node we claim to preceed

    """
    pass

def verify_finger_pos():  # Wikipedia's fix_fingers
    """Check each finger in the finger table to verify that node is alive if not
    recalcualtes finger at that ID

    """
    pass

