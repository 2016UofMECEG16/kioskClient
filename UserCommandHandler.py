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
	muKiosk = None
	Command = ''
	host = ''
	loginInfo = ''
	connected = False
	s_connected = False

	def __init__(self, myUI, myClient, myKiosk):
		self.myUI = myUI
		self.myClient = myClient
		self.myKiosk = myKiosk
	def execute(self, theCommand):
		action = theCommand[0:2]
		self.Command = theCommand[1:]
		takeaction = {
# TABLE OF TCP/IP CLIENT 
			"77": self.send,
			"c1": self.start,
		    "c2": self.connect,
		    "c3": self.disconnect,
		    "c4": self.send,
		    "c5": self.send,
		    "c6": self.send,
		    "c7": self.setHost,
		    "c8": self.serverLogin,
		    "c0": self.quit,
		    "C1": self.send,
# TABLE OF SCANNER COMMANDS
			"s1": self.scannerStart,
		    "s2": self.scannerConnect,
		    "s3": self.scannerDisconnect,
		    "s4": self.scannerSend,
		    "s5": self.scannerSend,
# TABLE OF MESSAGES TO SCANNER
			"S0": self.scannerSend, # BLANKS CARD
		    "S1": self.scannerSend, # POLLS FOR CARD
			"S2": self.scannerSend, # REGISTERS CARD
			"S3": self.scannerSend  # UPDATES CARD
			}
		if action == 'c7':
			self.host = theCommand[3:]
		if action == 'c8':
			self.loginInfo = theCommand[3:]
		if action == 's4':
			self.Command = theCommand[3:]
		takeaction.get(action, self.errhandler)()    

# COMMANDS TO CONTROL TCP/IP CLIENT
	def start (self):
		self.myClient.startClient()
	def connect (self):
		self.myClient.connect()
		self.connected = True
	def disconnect (self):
		self.myClient.disconnect()
		self.connected = False
	def send (self):
		self.myClient.sendMessageToServer(self.Command)
	def setHost(self):
		self.myClient.setHost(self.host)
	def serverLogin(self):
		self.myClient.sendMessageToServer(self.loginInfo)
	def quit (self):
		self.myClient.stopClient()
		self.myUI.exit()

# COMMANDS TO CONTROL SCANNER
	def scannerStart (self):
		self.myKiosk.startClient()
	def scannerConnect (self):
		self.myKiosk.connect()
		self.s_connected = True
	def scannerDisconnect (self):
		self.myKiosk.disconnect()
		self.s_connected = False
	def scannerSend (self):
		self.myKiosk.sendMessageToScanner(self.Command)

# COMMANDS FOR DEBUGGING
	def errhandler (self):
		print "User: Your input has not been recognised"