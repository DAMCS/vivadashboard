'''
Contains generic utils used in the System.
'''

import socket

def is_connected():
    '''
    Checks if a connection to the internet is available.
    Required for getting the required data from the forms.
    '''
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname("www.google.com")
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False
