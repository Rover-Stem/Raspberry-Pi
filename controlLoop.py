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

	else:

		storage.messagesOut.put("E,Not Valid Option or System Not Online or System Not Active")

def scrub (arr):

	arr = list(filter(None, arr))

	return arr

def parseLanguage (cmd):

	if (cmd[0] == "run"):

		cmd = "R"

		for i in range(0, len(cmd)):

			if (i == 0):

				continue

			cmd += "," + cmd[i]

		return cmd

	elif (cmd[0] == "rep"):

		return f"C,{cmd[1]}"

	elif (cmd[0] == "in"):

		return "I"

	elif (cmd[0] == "str"):

		return "S"

	elif (cmd[0] == "wt"):

		return f"W,{cmd[1]}"

	elif (cmd[0] == "for"):

		return "F"

	elif (cmd[0] == "if"):

		return f"L,{cmd[1]}"

	elif (cmd[0] == "br"):

		return "B"

	elif (cmd[0] == "pl"):

		return "P,logic"

	elif (cmd[0] == "pr"):

		return "P,loop"

	elif (cmd[0] == "e"):

		return "E"

	else:

		return f"A,{cmd[0]}"

def interpret (cmdSet):

	repeats = []
	loopPointers = []
	logicPointers = []

	loopEnds = []
	logicEnds = []

	currentPointer = 0

	input = ""
	store = ""

	while True:

		if (cmdSet[currentPointer][0] == "R"):

			switch(cmdSet[currentPointer])

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

		elif (cmdSet[currentPointer][0] == "I"):

			storage.messagesOut.put("I")

			while True:

				if not(storage.messagesIn.empty()):

					input = storage.messagesIn.get()

					break

		elif (cmdSet[currentPointer][0] == "S"):

			if (cmdSet[currentPointer][1] == "in"):

				store = input

			else:

				store = cmdSet[currentPointer][1]

		elif (cmdSet[currentPointer][0] == "W"):

			sleep(int(cmdSet[currentPointer][1]))

		elif (cmdSet[currentPointer][0] == "F"):

			if not(currentPointer in loopPointers):

				loopPointers.append(currentPointer)
				repeats.append(-1)
				loopEnds.append(-1)

		elif (cmdSet[currentPointer][0] == "L"):

			if not(currentPointer in logicPointers):

				logicPointers.append(currentPointer)

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

		elif (cmdSet[currentPointer][0] == "B"):

			for i in loopPointers:

				if (i > currentPointer):

					currentPointer = loopEnds[loopPointers.index(i)]

					break

		elif (cmdSet[currentPointer][0] == "P"):

			if (cmdSet[currentPointer][1] == "loop"):

				if not(currentPointer in loopEnds):

					for i in range(len(loopEnds) - 1, -1, -1):

						if (loopEnds[i] == -1):

							loopEnds[i] = currentPointer

				currentPointer = loopPointers[loopEnds.index(currentPointer)]

		elif (cmdSet[currentPointer][0] == "E"):

			break

		elif (cmdSet[currentPointer][0] == "A"):

			storage.messagesOut.put(f"E,Invalid Option For Code: {cmdSet[currentPointer][1]}")
			break

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

def runCmdSetStaged ():

	cmdSet = []

	while True:

		if not(storage.messagesIn.empty()):

			msg = storage.messagesIn.get()

			cmdSet.append(parseLanguage(msg))

			if (cmdSet[-1][0] == "E"):

				break

	interpret(cmdSet)

def runFile (filePath):

	cmdSet = []

	with open(filePath, 'r') as f:

		cmdSet = f.read().split("\n")

	for i in range(0, len(cmdSet)):

		cmdSet[i] = cmdSet[i].split(" ")

	cmdSet = scrub(cmdSet)

	print(cmdSet)

	for i in range(0, len(cmdSet)):

		cmdSet[i] = parseLanguage(cmdSet[i])

	interpret(cmdSet)

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

rover = rover()

# Options: Move, Move Distance, Move Servo, Get Distance, Get Average Distance, Get Mag, Get Accel, Take Picture, Redo All Systems, Redo Motors, Redo Camera, Redo Magnetometer and Accelerometer, Redo Servo, Redo Ultra Sonic Sensor, Status Update
presets = ["m", "md", "ms", "gd", "gad", "gm", "ga", "tp", "ra", "rm", "rc", "rma", "rs", "ru", "su"]

while True:

	if not(storage.messagesIn.empty()):

		cmd = storage.messagesIn.get()

		if (cmd == "stop"):

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