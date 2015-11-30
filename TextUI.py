########################################################################################
#																					   #
# TextUI																			   #
#																					   #
########################################################################################

from threading import Thread
import sys

class TextUI(Thread):

	console = None
	myCommandHandler = None

	def __init__(self):
		self.console = sys.stdin
		if self.console == None:
			print "Error, exiting program."
			sys.exit(0)

		Thread.__init__(self)

	def setCommand(self, myCommandHandler):
		self.myCommandHandler = myCommandHandler

	def getUserInput(self):
		userInput = "No input"
		try:
			userInput = raw_input()
			return userInput
		except IOError as e:
			print "Error reading from device, exiting program."
			sys.exit(0)

	def display(self, theResult):
		print theResult

	def run(self):
		while True:
			userInput = self.getUserInput()
			self.myCommandHandler.execute(userInput)