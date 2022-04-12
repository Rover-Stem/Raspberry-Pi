import os
import queue
import socket
import storage
import threading
import commandSet
import subprocess
import constantLogger

from time import sleep
from rover import rover
from server import server

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

def switch (cmd):

	if (cmd[1] in presets):

		if ((cmd[1] == presets[0]) and not(storage.status[0][2])):

			commandSet.move(cmd, rover)

		elif ((cmd[1] == presets[1]) and not(storage.status[0][2])):

			commandSet.moveDistance(cmd, rover)

		elif ((cmd[1] == presets[2]) and not(storage.status[3][2])):

			commandSet.moveServo(cmd, rover)

		elif ((cmd[1] == presets[3]) and not(storage.status[4][2])):

			commandSet.getDistance(cmd, rover)

		elif ((cmd[1] == presets[4]) and not(storage.status[4][2])):

			commandSet.getAverageDistance(cmd, rover)

		elif ((cmd[1] == presets[5]) and not(storage.status[2][2])):

			commandSet.getMag(cmd, rover)

		elif ((cmd[1] == presets[6]) and not(storage.status[2][2])):

			commandSet.getAccel(cmd, rover)

		elif ((cmd[1] == presets[7]) and not(storage.status[1][2])):

			commandSet.takePic(cmd, rover)

		elif (cmd[1] == presets[8]):

			commandSet.redoAll(cmd, rover)

		elif (cmd[1] == presets[9]):

			commandSet.redoMotors(cmd, rover)

		elif (cmd[1] == presets[10]):

			commandSet.redoCamera(cmd, rover)

		elif (cmd[1] == presets[11]):

			commandSet.redoMagAndAccel(cmd, rover)

		elif (cmd[1] == presets[12]):

			commandSet.redoServo(cmd, rover)

		elif (cmd[1] == presets[13]):

			commandSet.redoUltraSonic(cmd, rover)

		elif (cmd[1] == presets[14]):

			commandSet.statusUpdate(cmd, rover)

		elif (cmd[1] == presets[15]):

			commandSet.getDirection(cmd, rover)

	else:

		storage.messagesOut.put("E,Not Valid Option or System Not Online or System Not Active")

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

print("Hello")

#wifi = ""

#if ("raspberry" in socket.gethostname().lower()):

#	while True:

#		try:

#			output = subprocess.check_output(["sudo", "iwgetid"])
#			wifi = output.split('"')[1]

#			if not((wifi == "") or (wifi == " ")):

#				break

#		except:

#			continue

print("Starting Server")

server = server()

print("Server Started")

tServer = threading.Thread(target = server.run, args = [], daemon = True)
tServer.start()

print("Server Thread Started")

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

		elif (cmd[0] == "S"):

			tLog = threading.Thread(target = constantLogger.main, args = [], daemon = True)
			tLog.start()

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