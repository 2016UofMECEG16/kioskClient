########################################################################################
#																					   #
# ApplicationRun																	   #
#																					   #
########################################################################################

import TextUI
import KivyUI
import UserCommandHandler
import Client
import ServerCommandHandler
from threading import Thread

def Main():
	myKivyUI = KivyUI.KivyUI()
	#myUI = TextUI.TextUI()

	myServerCommand2 = ServerCommandHandler.ServerCommandHandler(myKivyUI)
	#myServerCommand = ServerCommandHandler.ServerCommandHandler(myUI)
	
	myClient2 = Client.Client('localhost', 5555, myServerCommand2)
	#myClient = Client.Client('localhost', 5555, myServerCommand)

	myCommand2 = UserCommandHandler.UserCommandHandler(myKivyUI, myClient2)
	#myCommand = UserCommandHandler.UserCommandHandler(myUI, myClient)
	
	myKivyUI.setCommand(myCommand2)
	#myUI.setCommand(myCommand)
	
	myKivyUI.run()
	#myUIThread = myUI.start()
	#myUI.display("1:\tStart Client\n2:\tConnect\n3:\tDisconnect\n4:\tQuit\n");

if __name__ == '__main__':
	Main()