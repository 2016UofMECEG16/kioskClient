########################################################################################
#																					   #
# ApplicationRun																	   #
#																					   #
########################################################################################

import TextUI
import UserCommandHandler
import Client
import ServerCommandHandler
from threading import Thread

def Main():
	myUI = TextUI.TextUI()
	myServerCommand = ServerCommandHandler.ServerCommandHandler(myUI)
	myClient = Client.Client('localhost', 5555, myServerCommand)
	myCommand = UserCommandHandler.UserCommandHandler(myUI, myClient)
	myUI.setCommand(myCommand)
	myUIThread = myUI.start()
	myUI.display("1:\tStart Client\n2:\tConnect\n3:\tDisconnect\n4:\tQuit\n");

if __name__ == '__main__':
	Main()