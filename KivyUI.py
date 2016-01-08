import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty

#GLOBAL VARIABLES
myCommandHandler = None

class LoginScreen(GridLayout):
	def __init__(self, **kwargs):
		super(LoginScreen, self).__init__(**kwargs)
		self.cols = 2

		self.add_widget(Label(text="Username:"))
		self.username = TextInput(multiline=False)
		self.add_widget(self.username)

		self.add_widget(Label(text="Password:"))
		self.password = TextInput(multiline=False, password=True)
		self.add_widget(self.password)

class AdminMenu(Screen):
	myCommand = myCommandHandler

	def updateCommand(self):
		self.myCommand = myCommandHandler
	pass

class Start(Screen):

	pass

class InsertCard(Screen):
	pass

class NewCustomerMenu(Screen):
	pass

class ExistingCustomerMenu(Screen):
	pass

class BalanceUpdate(Screen):
	pass

class MyScreenManager(ScreenManager):
	myCommand = myCommandHandler

	def updateCommand(self):
		self.myCommand = myCommandHandler

	CID = ObjectProperty(None)
	EMAIL = ObjectProperty(None)
	BALANCE = ObjectProperty(None)
	command = ''

	def register(self):
		self.command = '4 '
		self.command += '0000000001 '
		self.command += 'villard@myumanitoba.ca '
		self.command += '20'
		self.myCommand.execute(self.command)

	pass

presentation = Builder.load_file("manager.kv")

class KivyUI(App):

	def build(self):
		return presentation

	def setCommand(self, myCommandHandler2):
		global myCommandHandler
		myCommandHandler = myCommandHandler2

	def display(self, String):
		pass

	if __name__ == '__main__':
		KivyUI().run()