########################################################################################
#																					   #
# ServerCommandHandler																   #
#																					   #
########################################################################################

class ServerCommandHandler:
	myUI = None
	myClient = None

	def __init__(self, myUI):
		self.myUI = myUI
	
	def execute(self, myClient, theCommand):
		if theCommand == b'\xfe':
			self.myUI.display("Serverside: Kiosk disconnecting from Server...")
			myClient.disconnect()
			self.myUI.display("Serverside: Kiosk disconnected from Server.\n")