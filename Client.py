########################################################################################
#																					   #
# Client																			   #
#																					   #
########################################################################################

import AbstractClient
import socket
import sys
import threading
from threading import Thread

class Client(AbstractClient.AbstractClient):
    
    def __init__(self, host, port, myServerCommand):
        super(Client, self)
        self.myServerCommand = myServerCommand
        Thread.__init__(self)
        self._lock = threading.Lock()

    def handleMessageFromServer(self, theCommand):
        self.myServerCommand.execute(self, theCommand)