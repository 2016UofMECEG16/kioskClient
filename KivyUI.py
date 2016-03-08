########################################################################################
#																					   #
# KivyUI																			   #
#																					   #
########################################################################################

import time
import kivy
import xml.etree.ElementTree as ET
from decimal import *
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.animation import Animation
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.vkeyboard import VKeyboard

########################################################################################
#																					   #
# GLOBAL VARIABLES																	   #
#																					   #
########################################################################################

# DON'T USE GLOBAL VARIABLES IN OOP YOU DUMBASS

########################################################################################
#																					   #
# SCREEN COLLECTION																	   #
#																					   #
########################################################################################

# IMPLEMENTED SCREENS
class Bootup(Screen):
	fail_text = ObjectProperty('')
	def login(self, appLogin):
		if (appLogin == True):
			self.manager.current = "DemoMenu"
		else:
			self.fail_text = "Error: Login or Password is incorrect."
class DemoMenu(Screen):
	scanner_status = ObjectProperty('')
	connection_status = ObjectProperty('')
class ServerSettings(Screen):
	scanner_status = ObjectProperty('')
	connection_status = ObjectProperty('')
class ScannerSettings(Screen):
	scanner_status = ObjectProperty('')
	connection_status = ObjectProperty('')
class CustomerStart(Screen):
	title = ObjectProperty('')
	a = 0
class CustomerMenu(Screen):
	pass
class CustomerInsertBlank(Screen):
	message_label = ObjectProperty('')
class CustomerInsertExist(Screen):
	message_label = ObjectProperty('')
class CustomerInfo(Screen):
	message_label = ObjectProperty('')
	email_label = ObjectProperty('')
	balance_label = ObjectProperty('')
	cid_label = ObjectProperty('')
	device_label = ObjectProperty('')
class CustomerRegisterPay(Screen):
	purchase_label = ObjectProperty('')
	prev_screen = ObjectProperty('')
	email_label = ObjectProperty('')
class CustomerUpdatePay(Screen):
	purchase_label = ObjectProperty('')
	prev_screen = ObjectProperty('')
	email_label = ObjectProperty('')
class CustomerRegister(Screen):
	purchase_label = ObjectProperty('')
	message_label = ObjectProperty('')
class CustomerMenuExist(Screen):
	balance_label = ObjectProperty('')
	cid_label = ObjectProperty('')
class CustomerUpdateBalance(Screen):
	purchase_label = ObjectProperty('')
	email_label = ObjectProperty('')
	balance_label = ObjectProperty('')
	cid_label = ObjectProperty('')
class CustomerDelete(Screen):
	message_label = ObjectProperty('')
# PENDING SCREENS
class NewCustomerMenu(Screen):
	pass
class ExistingCustomerMenu(Screen):
	pass
# SCREEN MANAGER
class MyScreenManager(ScreenManager):
	con_sts = ObjectProperty('')
	scn_sts = ObjectProperty('')

	CIDLabel = ObjectProperty('')
	balanceLabel = ObjectProperty('')
	emailLabel = ObjectProperty('')
	messageLabel = ObjectProperty('')
	deviceLabel = ObjectProperty('')
	
	purchase = ObjectProperty('')
	email = ObjectProperty('')
	
	animation = Animation(pos=(0,-250), t='linear', duration=4.)
	animation += Animation(pos=(0,250), t='linear', duration=4.)
	animation.repeat = True
	def animate(self):
		self.current = "CustomerStart"
		#self.animation.start(self.get_screen('CustomerStart').title)
	def deanimate(self):
		self.current = "CustomerMenu"
		#Animation.stop_all(self.get_screen('CustomerStart').title)
	def updateConnectionStatus(self, status):
		self.con_sts = status
	def updateScannerStatus(self, status):
		self.scn_sts = status

	def updateMessageLabel(self, message):
		self.messageLabel = message

	def updateCustomerLabels(self, CID, balance, email, message, device):
		self.CIDLabel = CID
		self.balanceLabel = balance
		self.emailLabel = email
		self.messageLabel = message
		if device == "1":
			self.deviceLabel = "Card"
		else:
			self.deviceLabel = "Phone"
	def updatePayLabels(self, newPurchase, newEmail):
		self.purchase = newPurchase
		self.email = newEmail
	def increment(self, purchase, amount, screen):
		purchase =  Decimal(purchase) + amount
		purchaseLabel = str(purchase)
		self.get_screen(screen).purchase_label = purchaseLabel
	def decrement(self, purchase, amount, screen):
		if Decimal(purchase) > amount:
			purchase =  Decimal(purchase) - amount
		else:
			purchase = Decimal('0.00')
		purchaseLabel = str(purchase)
		self.get_screen(screen).purchase_label = purchaseLabel

########################################################################################
#																					   #
# APP																				   #
#																					   #
########################################################################################

class Customer:
	CID = ''
	balance = ''
	email = ''
	def __init__(self, CID, balance, email):
		self.CID = CID
		self.balance = balance
		self.email = email
	def changeCID(self, CID):
		self.CID = CID
	def changeBalance(self, balance):
		self.balance = balance
	def changeEmail(self, email):
		self.email = email
class KivyUI(App):

# CONFIGURATION
	Config.set('kivy', 'keyboard_mode', 'systemanddock')
	Config.set('kivy', 'keyboard_layout', 'email.json')
	Config.write()
# APP VARIABLES
	myCommand = None

	CID = "0"
	balance = "0.00"
	email = ""
	device = ""

	detected = False
	connected = False
	scannerConnected = False
	purchase = 0
	connectionStatus = "Disconnected"
	scannerStatus = "Disconnected"
	loginID = "admin"
	password = "password"

	tree = None
	root = None

	presentation = Builder.load_file("manager.kv")
# COMMON SCREEN FUNCTIONS
	def updateCIDValue(self, newCID):
		self.CID = newCID
	def updateConnectionStatus(self):
		if self.myCommand.connected:
			self.connected = True
			self.connectionStatus = "Connected"
		else:
			self.connected = False
			self.connectionStatus = "Disconnected"
	def updateScannerStatus(self):
		if self.myCommand.s_connected:
			self.scannerConnected = True
			self.scannerStatus = "Connected"
		else:
			self.scannerConnected = False 
			self.scannerStatus = "Disconnected"
	def sendToServer(self, text):
		self.myCommand.execute(text)
# BOOTUP FUNCTIONS
	def login(self, userLogin, userPassword):
		if (userLogin == self.loginID) & (userPassword == self.password):
			return True
		else:
			return False
# DEMO MENU FUNCTIONS
	def blankCard(self):
		self.myCommand.execute('S0')
	def cardBlanked(self):
		pass
# CACHE FUNCTIONS
	def updateCache(self):
		self.myCommand.execute('77')
		self.tree = ET.parse('database.xml')
		self.data = self.tree.getroot()
	def isCustomerInCache(self, custCID):
		isIn = False
		self.tree = ET.parse('database.xml')
		self.data = self.tree.getroot()
		for c in self.data.findall('Customer'):
			if (c.find('CID').text == custCID) or (('0'+c.find('CID').text) == custCID):
				isIn = True
		return isIn
	def getCustomerFromCache(self, custCID):
		self.tree = ET.parse('database.xml')
		self.data = self.tree.getroot()
		for c in self.data.findall('Customer'):
			if (c.find('CID').text == custCID) or (('0'+c.find('CID').text) == custCID):
				self.CID = custCID
				self.balance = "$%.2f" % float(c.find('Balance').text)
				self.email = c.find('Email').text
			else:
				pass
	def isEmailInCache(self, custEmail):
		isIn = False
		self.tree = ET.parse('database.xml')
		self.data = self.tree.getroot()
		for c in self.data.findall('Customer'):
			if (c.find('Email').text == custEmail):
				isIn = True
		return isIn
# CONNECTION SETTINGS FUNCTIONS 
	def setHost(self, HOST):
		command = 'c7 '
		command += HOST
		self.myCommand.execute(command)
	def serverConnect(self, serverID, serverPassword):
		self.myCommand.execute('c2')
		self.myCommand.execute('c8 '+serverID+' '+serverPassword)
	def serverDisconnect(self):
		self.myCommand.execute('c3')
# CUSTOMER MENU FUNCTIONS
	def scannerPoll(self):
		self.updateCache()
		time.sleep(1)
		self.myCommand.execute('S1')
# CUSTOMER MENU EXIST FUNCTIONS
	def cardRegistered(self):
		message = "Your pass has been successfully registered!"
		self.getCustomerFromCache(self.CID)
		self.presentation.updateCustomerLabels(self.CID, self.balance, self.email, message, "1")
		self.presentation.current = "CustomerInfo"
	def cardUpdated(self):
		message = "Your balance has been updated!"
		self.getCustomerFromCache(self.CID)
		self.presentation.updateCustomerLabels(self.CID, self.balance, self.email, message, self.device)
		self.presentation.current = "CustomerInfo"
# CUSTOMER INSERT BLANK FUNCTIONS
	def detectedIncorrect(self):
		self.presentation.updateMessageLabel("This NFC pass is not a properly formatted E-Pass.")
	def detectedBlank(self):
		if self.presentation.current == "CustomerInsertBlank":
			self.presentation.current = "CustomerRegister"
		else:
			self.presentation.updateMessageLabel("This pass is blank.")
# CUSTOMER INSERT EXIST FUNCTIONS
	def detectedExisting(self, CID, device):
		if self.isCustomerInCache(CID):
			if self.presentation.current == "CustomerInsertExist":
				self.CID = CID
				self.device = device
				self.getCustomerFromCache(CID)
				self.presentation.updateCustomerLabels(self.CID, self.balance, self.email, "", self.device)
				self.presentation.current = "CustomerInfo"
			else:
				self.presentation.updateMessageLabel("This pass is already in use.")
		else:
			self.presentation.updateMessageLabel("This pass was reported lost/broken and has been removed from the database.")
# CUSTOMER REGISTER FUNCTIONS
	def register(self, EMAIL, PURCHASE):
		if self.scannerConnected:
			self.CID = "0"
			command = 'c4 '
			command += EMAIL + ' '
			command += PURCHASE
			self.myCommand.execute(command)
			time.sleep(1.5)
			self.updateCache()
			time.sleep(1)
			command = 'S2' + self.CID + PURCHASE
			self.myCommand.execute(command)
		else:
			pass
	def getServerCID(self, newCID):
		self.CID = newCID
# CUSTOMER UPDATE BALANCE FUNCTIONS
	def update(self, PURCHASE):
		command = 'c5 '
		command += self.CID + ' '
		command += PURCHASE
		self.myCommand.execute(command)
		time.sleep(1.5)
		self.updateCache()
		time.sleep(1)
		command = 'S3' + PURCHASE
		self.myCommand.execute(command)
# CUSTUMER DELETE FUNCTIONS
	def delete(self, EMAIL):
		command = 'c6 '
		command += EMAIL
		self.myCommand.execute(command)
		time.sleep(1.5)
		self.updateCache()
# APP FUNCTIONS
	def build(self):
		return self.presentation
	def setCommand(self, myCommandHandler):
		self.myCommand = myCommandHandler
	def display(self, String):
		pass
	def exit(self):
		App.get_running_app().stop()	
	if __name__ == '__main__':
		KivyUI().run()
# END OF PROGRAM