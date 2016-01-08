########################################################################################
#																					   #
# UserCommandHandler																   #
#																					   #
########################################################################################

import socket
import sys
import threading

class UserCommandHandler:
	myUI = None
	myClient = None

	def __init__(self, myUI, myClient):
		self.myUI = myUI
		self.myClient = myClient

	def execute(self, theCommand):
		msg = b''
		temp = ""
		takeaction = {
			"1": self.start,
		    "2": self.connect,
		    "3": self.disconnect,
		    "4": self.quit,
		    "5": self.register}
		takeaction.get(theCommand, self.errhandler)()    

	def start (self):
		self.myClient.startClient()
		self.myUI.display("User: Client socket opened.")

	def connect (self):
	    self.myUI.display("User: Connecting client to Server...")
	    self.myClient.connect()
	    self.myUI.display("User: Connection to server established.")

	def disconnect (self):
	    self.myUI.display("User: Disconnecting client from Server...")
	    self.myClient.disconnect()
	    self.myUI.display("User: Disconnected from Server.")

	def quit (self):
		self.myClient.stopClient()
		self.myUI.display("User: Quitting program.")
		sys.exit(0)

	def register (self, line):
		self.myClient.sendMessageToServer(line)

	def errhandler (self):
		self.myUI.display("User: Your input has not been recognised")