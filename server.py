import time
import queue
import socket
import storage
import datetime
import threading

class server ():

	def __init__ (self, host = "", port = 1234, packetSize = 1024):

		storage.now = datetime.datetime.utcnow().strftime("%m-%d-%Y--%H:%M:%S")

		self.__logFile = f"logs/{storage.now}.log"

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

		self.__sockt.listen()

		while (True):

			try:

				conn, addr = self.__sockt.accept()

				print("Connected")

				conn.setblocking(True)

				if not(conn in connections):

					t_recv = threading.Thread(target = self.receiveMessages, args = [conn], daemon = True)
					t_recv.start()

					t_send = threading.Thread(target = self.sendMessages, args = [conn], daemon = True)
					t_send.start()

					connections.append(conn)

			except:

				if (conn == None):

					time.sleep(.1)

	def receiveMessages (self, conn):

		data = None

		firstMessageProccesed = False

		while (True):

			data = conn.recv(self.__packetSize)

			if data:

				if not(firstMessageProccesed):

					if (str(data, 'utf-8') == "T"):

						storage.testing = True
						storage.status = [["M", True, False], ["C", True, False], ["A", True, False], ["S", True, False], ["U", True, False]]

						firstMessageProccesed = True

						continue

					else:

						storage.testing = False
						firstMessageProccesed = True

						continue

				storage.messagesIn.put(str(data, 'utf-8'))

				if not(storage.testing):

					with open(self.__logFile, 'a+') as f:

						f.write(f"{datetime.datetime.utcnow().timestamp()} - Recieved: {str(data, 'utf-8')}\n")

				else:

					print(f"Recieved: {str(data, 'utf-8')}")

				if (str(data, 'utf-8') == "stop"):

					storage.messagesOut.put("stop")

					break

	def sendMessages (self, conn):

		while (True):

			if not(storage.messagesOut.empty()):

				msg = bytes(storage.messagesOut.get(), 'utf-8')

				if not(str(msg, 'utf-8') == "file"):

					conn.send(msg)

					if not(storage.testing):

						with open(self.__logFile, 'a+') as f:

							f.write(f"{datetime.datetime.utcnow().timestamp()} - Sent: {str(msg, 'utf-8')}\n")

					else:

						print(f"Sent: {str(msg, 'utf-8')}")

					if (str(msg, 'utf-8') == "stop"):

						conn.shutdown(SHUT_RDWR)

						conn.close()

						break

				else:

					conn.send(msg)

					if not(storage.testing):

						with open(self.__logFile, 'a+') as f:

							f.write(f"{datetime.datetime.utcnow().timestamp()} - Starting File Send\n")

					else:

						print(f"Starting File Send")

					filepath = storage.messagesOut.get()
					filename = filepath.split("/")[-1]

					if not(storage.testing):

						with open(self.__logFile, 'a+') as f:

							f.write(f"{datetime.datetime.utcnow().timestamp()} - Sending {filename}\n")

					else:

						print(f"Sending {filename}")

					conn.send(bytes(filename, 'utf-8'))

					with open(filepath, "rb") as f:

						while True:

							bytes_read = f.read(__packetSize)

							if not bytes_read:

								break

							conn.sendall(bytes_read)