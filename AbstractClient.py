########################################################################################
#                                                                                      #
# AbstractClient                                                                       #
#                                                                                      #
########################################################################################

from abc import ABCMeta, abstractmethod
import socket
import sys
import threading
from threading import Thread

class AbstractClient(Thread):

    HOST = 'localhost'       # The remote host
    PORT = 5555              # The same port as used by the server
    s = None
    serverS = None
    doConnect = False
    myServerCommand = None
    __metaclass__ = ABCMeta

    @abstractmethod
    def handleMessageFromServer(self, theCommand):
        """Handle message from ServerConnection thread."""

    def __init__(self, host, port, myServerCommand):

        self.HOST = host
        self.PORT = port
        self.myServerCommand = myServerCommand

        Thread.__init__(self)
        self._lock = threading.Lock()

    def startClient(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.start()
        except Exception as e:
            raise e
            sys.exit(0) 
        finally:
            pass

    def stopClient(self):
        if self.s != None:
            try:
                self.s.close()
            except Exception as e:
                raise e
                sys.exit(0)
            finally:
                pass

    def connect(self):
        if self.s != None:
            try:
                self.setDoConnect(True)
                self.s.settimeout(500)
                self.s.connect((self.HOST, self.PORT))
            except Exception as e:
                raise e
                sys.exit(0)
            finally:
                pass

    def setDoConnect(self, doConnect):
        with self._lock:
            self.doConnect = doConnect
            pass

    def disconnect(self):
        msg = b'\xfe'
        if self.s != None:
            try:
                self.s.send(msg)
                self.setDoConnect(False)
                self.s.settimeout(5000)
                self.s.close()
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except Exception as e:
                raise e
                sys.exit(0)
            finally:
                pass

    def getMessageFromServer(self):
        try:
            msg = self.s.recv(1024)
            return msg
        except Exception, e:
            raise e
            sys.exit(0)
        finally:
            pass

    def sendMessageToServer(self, msg):
        try:
            self.s.send(msg)
        except IOException, e:
            raise e
            sys.exit(0)
        finally:
            pass

    def run(self):
        while self.doConnect:
            msg = self.getMessageFromServer()
            self.handleMessageFromServer(msg)
        return