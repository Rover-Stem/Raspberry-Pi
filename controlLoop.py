import queue
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

	else:

		storage.messagesOut.put("E,Not Valid Option or System Not Online or System Not Active")

def parseCmd (cmd):

	if ("-" in cmd):

		if ("," in cmd):

			cmd = cmd.split("-")
			cmd = cmd.split(",")

			args = ""

			for i in cmd[1]:

				args += "," + i

			cmd = f"R,{cmd[0]}" + args

		else:

			cmd = cmd.replace("-", ",")

			cmd = f"R,{cmd}"

	return cmd

def parseCmdSet ():

	while True:

		if not(storage.messagesIn.empty()):

			cmd = storage.messagesIn.get()

			if (cmd[0] == "e"):

				break

			elif not(cmd[0] == "r"):

				switch(parseCmd(cmd))

				storage.messagesOut.put("F")

			else:

				# TODO: Need to add for loop functionality

				repeats = cmd.split(" ")[1]

				cmdList = []

				while True:

					if not(storage.messagesIn.empty()):

						cmd = storage.messagesIn.get()

						if (cmd == "fe"):

							break

						cmdList.append(parseCmd(cmd))

				for i in range(repeats):

					for cmd in cmdList:

						switch(cmd)

				storage.messagesOut.put("F")

wifi = ""

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

rover = rover()

# Options: Move, Move Distance, Move Servo, Get Distance, Get Average Distance, Get Mag, Get Accel, Take Picture, Redo All Systems, Redo Motors, Redo Camera, Redo Magnetometer and Accelerometer, Redo Servo, Redo Ultra Sonic Sensor
presets = ["m", "md", "ms", "gd", "gad", "gm", "ga", "tp", "ra", "rm", "rc", "rma", "rs", "ru"]

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

			parseCmdSet()