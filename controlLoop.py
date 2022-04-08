import os
import queue
import socket
import storage
import interpret
import threading
import commandSet
import subprocess

from time import sleep
from rover import rover
from server import server
from switcher import switch

# Sorts list by file type
def sortByFileType (arr):

	temp = [[[], "a"]]
	temp2 = []

	for i in arr:

		if (i.split(".")[-1] in [x[1] for x in temp]):

			for j in temp:

				if ((i.split(".")[-1] == j[1]) and not(i.split(".")[0] == j[1])):

					j[0].append(i)

		else:

			if (i.split(".")[0] == i.split(".")[-1]):

				for j in temp:

					if (j[1] == "a"):

						j[0].append(i)

			else:

				temp.append([[i], i.split(".")[-1]])

	for j in temp:

		j[0].sort()

	fileTypes = [x[1] for x in temp]

	fileTypes.sort()

	for i in fileTypes:

		for j in temp:

			if j[1] == i:

				for l in j[0]:

					temp2.append(l)

				break

		continue

	return temp2

# Helper method to remove empty entries from given array - [[""], ["a"], ["run"]] -> [["a"], ["run"]]
def scrub (arr):

	temp_array = arr

	for i in range(len(arr) - 1, -1, -1):

		for j in range(len(arr[i])):

			temp_array[i][j] = temp_array[i][j].replace(" ", "")
			temp_array[i][j] = temp_array[i][j].replace("\t", "")

		if (temp_array[i][0] == ""):

			temp_array.pop(i)

	return arr

# Remote control
def liveRun ():

	storage.messagesOut.put("I")

	input = ""

	while True:

		if not(storage.messagesIn.empty()):

			input = storage.messagesIn.get()

			if (input == "e"):

				break

			elif (input == "\x1b[A"):

				switch(["R", "m", "f", -1])

			elif (input == "\x1b[B"):

				switch(["R", "m", "b", -1])

			elif (input == "\x1b[C"):

				switch(["R", "m", "r", -1])

			elif (input == "\x1b[D"):

				switch(["R", "m", "l", -1])

			else:

				switch(["R", "m", "s"])

	storage.messagesOut.put("F")

# Logic for file control
def multiCmd (cmd):

	try:

		if not((cmd[1] == "l") or (cmd[1] == "s")):

			filePath = cmd[1]

			if not("squish" in filePath):

				return

			interpret.runFile(filePath, rover)

		elif (cmd[1] == "l"):

			liveRun()

		else:

			interpret.runCmdSetStaged(rover)

	except:

		interpret.runCmdSetStaged(rover)

wifi = ""

if ("raspberry" in socket.gethostname().lower()):

	while True:

		try:

			output = subprocess.check_output(["sudo", "iwgetid"])
			wifi = output.split('"')[1]

			if not((wifi == "") or (wifi == " ")):

				break

		except:

			continue

server = server()

tServer = threading.Thread(target = server.run, args = [], daemon = True)
tServer.start()

while True:

	if not(storage.testing == None):

		break

if (storage.testing):

	print("Started")

else:

	import constantLogger

	constantLogger.main()

rover = rover()

# Options: Move, Move Distance, Move Servo, Get Distance, Get Average Distance, Get Mag, Get Accel, Take Picture, Redo All Systems, Redo Motors, Redo Camera, Redo Magnetometer and Accelerometer, Redo Servo, Redo Ultra Sonic Sensor, Status Update, Get Direction
presets = ["m", "md", "ms", "gd", "gad", "gm", "ga", "tp", "ra", "rm", "rc", "rma", "rs", "ru", "su", "gdir"]

while True:

	if not(storage.messagesIn.empty()):

		cmd = storage.messagesIn.get()

		if (cmd == "stop"):

			storage.exiting = True

			break

		else:

			cmd = cmd.split(",")

		if (cmd[0] == "R"):

			switch(cmd)

			storage.messagesOut.put("F")

		elif (cmd[0] == "F"):

			multiCmd(cmd)

			storage.messagesOut.put("F")

		elif (cmd[0] == "L"):

			try:

				programsList = []

				for i in os.listdir(f"./{cmd[1]}"):

					programsList.append(i + "")

				programsList = sortByFileType(programsList)

				storage.messagesOut.put("S,L,Files in this directory:")

				for i in programsList:

					storage.messagesOut.put("S,L," + i)

					if (storage.testing):

						sleep(0.07)

					else:

						sleep(0.01)

				storage.messagesOut.put("F")

			except Exception as e:

				if (storage.testing):

					print(e)

				storage.messagesOut.put("E,File Path Error")
				storage.messagesOut.put("F")