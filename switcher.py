import commandSet

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
