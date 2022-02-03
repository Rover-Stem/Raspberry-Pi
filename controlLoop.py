import os
import queue
import socket
import storage
import threading
import commandSet
import subprocess

from time import sleep
from rover import rover
from server import server

# Sends Commands to Command Set
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

# Helper method to remove empty entries from given array - [[""], ["a"], ["run"]] -> [["a"], ["run"]]
def scrub (arr):

	temp_array = arr

	for i in range(len(arr) - 1, -1, -1):

		if (temp_array[i][0] == ""):

			temp_array.pop(i)

	return arr

# Goes from psuedo language to comms commands
def parseLanguage (cmd):

	if (cmd[0] == "run"):

		cmd = "R"

		for i in range(0, len(cmd)):

			if (i == 0):

				continue

			cmd += "," + cmd[i]

		return cmd

	elif (cmd[0] == "rep"):

		return ["C", int(cmd[1])]

	elif (cmd[0] == "in"):

		return "I"

	elif (cmd[0] == "str"):

		return ["S", int(cmd[1])]

	elif (cmd[0] == "wt"):

		return ["W", int(cmd[1])]

	elif (cmd[0] == "for"):

		return "F"

	elif (cmd[0] == "if"):

		return ["L", cmd[1], cmd[2]]

	elif (cmd[0] == "br"):

		return "B"

	elif (cmd[0] == "pl"):

		return ["P", "logic"]

	elif (cmd[0] == "pr"):

		return ["P", "loop"]

	elif (cmd[0] == "e"):

		return "E"

	elif (cmd[0] == "add"):

		return ["A", int(cmd[1])]

	else:

		return ["K", cmd[0]]

# Running logic for parsed commands
def interpret (cmdSet):

	repeats = []
	loopPointers = []
	logicPointers = []

	loopEnds = []
	logicEnds = []

	currentPointer = 0

	input = ""
	store = 0

	while True:

		# Runs Command
		if (cmdSet[currentPointer][0] == "R"):

			switch(cmdSet[currentPointer])

		# Adds to store
		elif (cmdSet[currentPointer][0] == "A"):

			store += cmdSet[currentPointer][1]

		# Assigns rep loop pointers and counts down
		elif (cmdSet[currentPointer][0] == "C"):

			if not(currentPointer in loopPointers):

				loopPointers.append(currentPointer)
				repeats.append(int(cmdSet[currentPointer][1]) - 1)
				loopEnds.append(-1)

			else:

				if (repeats[loopPointers.index(currentPointer)] == 0):

					index = loopPointers.index(currentPointer)

					loopPointers.pop(index)
					repeats.pop(index)

					currentPointer = loopEnds[index] + 1

					loopEnds.pop(index)

				else:

					repeats[loopPointers.index(currentPointer)] -= 1

		# Gets input
		elif (cmdSet[currentPointer][0] == "I"):

			storage.messagesOut.put("I")

			while True:

				if not(storage.messagesIn.empty()):

					input = storage.messagesIn.get()

					break

		# Stores input val or val after statement
		elif (cmdSet[currentPointer][0] == "S"):

			if (cmdSet[currentPointer][1] == "in"):

				store = input

			else:

				store = cmdSet[currentPointer][1]

		# Waits
		elif (cmdSet[currentPointer][0] == "W"):

			sleep(int(cmdSet[currentPointer][1]))

		# Sets up loop pointers for forever loops
		elif (cmdSet[currentPointer][0] == "F"):

			if not(currentPointer in loopPointers):

				loopPointers.append(currentPointer)
				repeats.append(-1)
				loopEnds.append(-1)

		# Sets up if statement pointer
		elif (cmdSet[currentPointer][0] == "L"):

			if not(currentPointer in logicPointers):

				logicPointers.append(currentPointer)

				# # TODO: Make go backwards and be better
				for i in range(currentPointer, len(cmdSet)):

					if ((cmdSet[i][0] == "P") and (cmdSet[i][1] == "logic")):

						logicEnds.append(i)

						break

			if (cmdSet[currentPointer][1] == "in"):

				if (store == input):

					continue

				else:

					index = logicPointers.index(currentPointer)

					currentPointer = logicEnds[index] + 1

					logicEnds.pop(index)
					logicPointers.pop(index)

			else:

				try:

					if (store == int(cmdSet[currentPointer][1])):

						continue

					else:

						index = logicPointers.index(currentPointer)

						currentPointer = logicEnds[index] + 1

						logicEnds.pop(index)
						logicPointers.pop(index)

				except:

					if (store == cmdSet[currentPointer][1]):

						continue

					else:

						index = logicPointers.index(currentPointer)

						currentPointer = logicEnds[index] + 1

						logicEnds.pop(index)
						logicPointers.pop(index)

		# BReaks
		elif (cmdSet[currentPointer][0] == "B"):

			for i in loopPointers:

				# TODO: Wrong logic. Must find closest loop
				if (i > currentPointer):

					currentPointer = loopEnds[loopPointers.index(i)] + 1

					break

		# Sets up endings and looping
		elif (cmdSet[currentPointer][0] == "P"):

			if (cmdSet[currentPointer][1] == "loop"):

				if not(currentPointer in loopEnds):

					for i in range(len(loopEnds) - 1, -1, -1):

						if (loopEnds[i] == -1):

							loopEnds[i] = currentPointer

				currentPointer = loopPointers[loopEnds.index(currentPointer)]

		# Ends Program
		elif (cmdSet[currentPointer][0] == "E"):

			break

		# Adjusts for unknown commands
		elif (cmdSet[currentPointer][0] == "K"):

			storage.messagesOut.put(f"E,Invalid Option For Code: {cmdSet[currentPointer][1]}")
			break

# Remote control
def liveRun ():

	storage.messagesOut.put("I")

	input = ""

	while True:

		if not(storage.messagesIn.empty()):

			input = storage.messagesIn.get()

			if (input == "\x1b[A"):

				switch("R,m,f,-1")

			elif (input == "\x1b[B"):

				switch("R,m,b,-1")

			elif (input == "\x1b[C"):

				switch("R,m,r,-1")

			elif (input == "\x1b[D"):

				switch("R,m,l,-1")

			else:

				switch("R,m,s")

# Gets remote file sent and then runs it
def runCmdSetStaged ():

	cmdSet = []

	while True:

		if not(storage.messagesIn.empty()):

			msg = storage.messagesIn.get()

			cmdSet.append(parseLanguage(msg))

			if (cmdSet[-1][0] == "E"):

				break

	interpret(cmdSet)

# Runs local file
def runFile (filePath):

	cmdSet = []

	try:

		with open(filePath, 'r') as f:

			cmdSet = f.read().split("\n")

	except:

		storage.messagesOut.put("E,File Path Non-Existent")
		storage.messagesOut.put("F")

	for i in range(0, len(cmdSet)):

		cmdSet[i] = cmdSet[i].split(" ")

	cmdSet = scrub(cmdSet)

	print(cmdSet)

	for i in range(0, len(cmdSet)):

		cmdSet[i] = parseLanguage(cmdSet[i])

	print(cmdSet)

	interpret(cmdSet)

# Logic for file control
def multiCmd (cmd):

	try:

		if not((cmd[1] == "l") or (cmd[1] == "s")):

			filePath = cmd[1]

			runFile(filePath)

		elif (cmd[1] == "l"):

			liveRun()

		else:

			runCmdSetStaged()

	except:

		runCmdSetStaged()

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

				programsList.sort()

				storage.messagesOut.put("S,L,Files in this directory:")

				for i in programsList:

					storage.messagesOut.put("S,L," + i)
					sleep(0.01)

				storage.messagesOut.put("F")

			except Exception as e:

				if (storage.testing):

					print(e)

				storage.messagesOut.put("E,File Path Error")
				storage.messagesOut.put("F")