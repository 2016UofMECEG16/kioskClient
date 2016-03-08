########################################################################################
#																					   #
# ServerCommandHandler																   #
#																					   #
########################################################################################

class ServerCommandHandler:
	myUI = None
	myClient = None
	message = ""
	database = None
	CID = None
	time = None

	def __init__(self, myUI):
		self.myUI = myUI
	
	def execute(self, myClient, theCommand):
		if theCommand == chr(-2+256):
			self.myUI.display("Serverside: Kiosk disconnecting from Server...")
			myClient.disconnect()
			self.myUI.display("Serverside: Kiosk disconnected from Server.\n")
		elif theCommand == chr(126):
			pass
		elif theCommand == chr(127):
			self.database = open('database.xml', 'w')
			self.database.write('<?xml version="1.0"?>\n')
		elif theCommand == chr(130):
			self.CID = "hi"
		elif theCommand == chr(131):
			self.time = "hi"
		elif theCommand == chr(-128+256): # chr(128)
			if self.CID != None:
				self.myUI.getServerCID(self.message)
				self.CID = None
			if self.time != None:
				self.myUI.setTime(self.message)
				self.time = None
			if self.database != None:
				if self.database.closed != True:
					self.database.write(self.message)
					self.database.close()
			elif self.message[0:4] == "ack0":
				self.myUI.cardBlanked()
			elif self.message[0:4] == "ack1":
				if self.message[4] == "1":
					self.myUI.detectedIncorrect()
				elif self.message[4] == "2":
					self.myUI.detectedBlank()
				elif self.message[4] == "3":
					self.myUI.detectedExisting(self.message[5:15], self.message[15])
			elif self.message[0:4] == "ack2":
				self.myUI.cardRegistered()
			elif self.message[0:4] == "ack3":
				self.myUI.cardUpdated()
			self.message = ""
		elif theCommand == chr(-127+256): # chr(129)
			self.myClient.disconnect()
		else:
			self.message += str(theCommand)