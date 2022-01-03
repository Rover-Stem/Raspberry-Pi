import time
import queue
import socket
import storage
import threading

class server ():

	def __init__ (self, host = "", port = 29500, packetSize = 1024):

		self.__host = host
		self.__port = port
		self.__packetSize = packetSize

		self.__sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__sockt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.__sockt.bind((self.__host, self.__port))
		self.__sockt.setblocking(False)

	def run (self):

		connections = []
		t_recv = None
		t_send = None
		conn = None

		self.__sockt.listen(1)

		while (True):

			try:

				conn, addr = self.__sockt.accept()

				conn.setblocking(True)

				if not(conn in connections):

					t_recv = threading.Thread(target = self.receiveMessages, args = [conn], daemon = True)
					t_recv.start()

					t_send = threading.Thread(target = self.sendMessages, args = [conn], daemon = True)
					t_send.start()

					connections.append(conn)

			except:

				if (conn == None):

					time.sleep(1)

	def receiveMessages (self, conn):

		data = None

		while (True):

			data = conn.recv(self.__packetSize)

			if data:

				storage.messagesIn.put(str(data, 'utf-8'))

				print(str(data, 'utf-8'))

				if (str(data, 'utf-8') == "stop"):

					storage.messagesOut.put("stop")

					break

	def sendMessages (self, conn):

		while (True):

			if not(storage.messagesOut.empty()):

				msg = bytes(storage.messagesOut.get(), 'utf-8')

				conn.send(msg)

				if (str(msg, 'utf-8') == "stop"):

					conn.shutdown(conn.SHUT_RDWR)

					conn.close()

					break