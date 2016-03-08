########################################################################################
#																					   #
# ApplicationRun																	   #
#																					   #
########################################################################################

import KivyUI
import UserCommandHandler
import Client
import ServerCommandHandler

from threading import Thread

# scannerIP = '192.169.0.32'
# scannerIP = '10.42.0.49'
scannerIP = 'localhost'

def Main():
	myKivyUI			= KivyUI.KivyUI()
	myServerCommand		= ServerCommandHandler.ServerCommandHandler(myKivyUI)
	myClient			= Client.Client('', 5555, myServerCommand)
	myScannerCommand	= ServerCommandHandler.ServerCommandHandler(myKivyUI)
	myKiosk				= Client.Client(scannerIP, 5556, myScannerCommand)
	myCommand			= UserCommandHandler.UserCommandHandler(myKivyUI, myClient, myKiosk)
	myKivyUI.setCommand(myCommand)
	myKivyUI.run()

if __name__ == '__main__':
	Main()
