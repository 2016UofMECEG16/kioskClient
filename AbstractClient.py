########################################################################################
#                                                                                      #
# AbstractClient                                                                       #
#                                                                                      #
########################################################################################

from abc import ABCMeta, abstractmethod
import socket
import sys
import threading
from threading import Thread

class AbstractClient(Thread):

	HOST = ''
	PORT = None
	s = None
	serverS = None
	doConnect = False
	connected = False
	__metaclass__ = ABCMeta

	@abstractmethod
	def handleMessageFromServer(self, theCommand):
		"""Handle message from ServerConnection thread."""
		pass

	def __init__(self, host, port):
		self.HOST = host
		self.PORT = port
		Thread.__init__(self)
		self._lock = threading.Lock()
	def setHost(self, host):
		self.HOST = host
	def startClient(self):
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except Exception as e:
			raise e
			sys.exit(0) 
		finally:
			pass
	def stopClient(self):
		if self.s != None:
			try:
				self.s.close()
			except Exception as e:
				raise e
				sys.exit(0)
			finally:
				pass
	def connect(self):
		if self.s != None:
			try:
				self.setDoConnect(True)
				self.s.settimeout(None)
				self.s.connect((self.HOST, self.PORT))
				self.start()
				self.connected = True
			except Exception as e:
				pass
			finally:
				pass
	def setDoConnect(self, doConnect):
		with self._lock:
			self.doConnect = doConnect
			pass
	def disconnect(self):
		msg = b'\xff'
		if self.s != None:
			try:
				self.s.send(msg)
				self.setDoConnect(False)
				self.s.settimeout(5000)
				self.s.close()
				self.connected = False
				self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			except Exception as e:
				raise e
				sys.exit(0)
			finally:
				pass
	def getMessageFromServer(self):
		try:
			msg = self.s.recv(1)
			return msg
		except Exception, e:
			raise e
			sys.exit(0)
		finally:
			pass
	def sendMessageToServer(self, msg):
		try:
			self.s.send(msg)
			self.s.send(b'\x80')
		except IOException, e:
			raise e
			sys.exit(0)
		finally:
			pass
	def sendMessageToScanner(self, msg):
		try:
			self.s.send(msg)
		except IOException, e:
			raise e
			sys.exit(0)
		finally:
			pass
	def run(self):
		while self.doConnect:
			msg = self.getMessageFromServer()
			self.handleMessageFromServer(msg)
		threading.Thread.__init__(self)
