import queue
import storage

from time import sleep

def move (cmd, rover):

	try:

		time = float(cmd[3])

	except:

		time = 1

	try:

		ratio = float(cmd[4])

		try:

			throttle = float(cmd[5])

			if ((throttle > 1) or (throttle < 0)):

				storage.messagesOut.put("E,Throttle Must Be Between 1 and 0 (inclusive)")

				return

			if (((ratio > 1) and ((throttle * ratio) > 1)) or (ratio < 0)):

				storage.messagesOut.put("E,Ratio Must Not Result In A Trottle Greater Than 1 And Must Not Be Negative")

				return

			rover.moveRover(cmd[2], ratio, throttle)

			if not(time == -1):

				sleep(time)

				rover.moveRover("s")

			return

		except:

			rover.moveRover(cmd[2], ratio)

			if not(time == -1):

				sleep(time)

				rover.moveRover("s")

			return

	except:

		rover.moveRover(cmd[2])

		if not(time == -1):

			sleep(time)

			rover.moveRover("s")

		return

def moveDistance (cmd, rover):

	try:

		distance = float(cmd[2])

		try:

			cm = bool(cmd[3])

			rover.moveDistance(distance, cm)

			return

		except:

			rover.moveDistance(distance)

			return

	except:

		storage.messagesOut.put("E,Distance Must Be Provided")

		return

def moveServo (cmd, rover):

	try:

		angle = float(cmd[2])

		if ((angle > 1) or (angle < -1)):

			storage.messagesOut.put("E,Angle Must Be Between 1 and -1 (inclusive)")

			return

		rover.moveServo(angle)

		return

	except Exception as e:

		storage.messagesOut.put("E,Angle Must Be Provided")
		storage.messagesOut.put(f"E,{e}")

		return

def getDistance (cmd, rover):

	distance = rover.getDistance()

	storage.messagesOut.put(f"S,D,{distance}")

	return

def getAverageDistance (cmd, rover):

	try:

		pulse_wait = cmd[2]

		try:

			numPulses = cmd[3]

			avrDistance = rover.getAvrDistance(pulse_wait, numPulses)

			storage.messagesOut.put(f"S,AD,{avrDistance},{numPulses},{pulse_wait}")

			return

		except:

			avrDistance = rover.getAvrDistance(pulse_wait)

			storage.messagesOut.put(f"S,AD,{avrDistance},5,{pulse_wait}")

			return

	except:

		avrDistance = rover.getAvrDistance()

		storage.messagesOut.put(f"S,AD,{avrDistance},5,0.0001")

		return

def getMag (cmd, rover):

	mag = rover.getMag()

	storage.messagesOut.put(f"S,M,{mag[0]},{mag[1]},{mag[2]}")

	return

def getAccel (cmd, rover):

	accel = rover.getAccel()

	storage.messagesOut.put(f"S,A,{accel[0]},{accel[1]},{accel[2]}")

	return

def takePic (cmd, rover):

	rover.takePic()

	return

def redoMotors (cmd, rover):

	rover.redoMotors()

	storage.messagesOut.put(f"S,Motors Reset")

	return

def redoCamera (cmd, rover):

	rover.redoCamera()

	storage.messagesOut.put(f"S,Camera Reset")

	return

def redoMagAndAccel (cmd, rover):

	rover.redoMagAndAccel()

	storage.messagesOut.put(f"S,Magnetometer And Accelerometer Reset")

	return

def redoServo (cmd, rover):

	rover.redoServo()

	storage.messagesOut.put(f"S,Servo Reset")

	return

def redoUltraSonic (cmd, rover):

	rover.redoUltraSonic()

	storage.messagesOut.put(f"S,Ultra Sonic Sensor Reset")

	return

def redoAll (cmd, rover):

	rover.redoMotors()
	rover.redoCamera()
	rover.redoMagAndAccel()
	rover.redoServo()
	rover.redoUltraSonic()

	storage.messagesOut.put(f"S,All Reset")

	return

def statusUpdate (cmd, rover):

	rover.statusUpdate()

	return

def getDirection (cmd, rover):

	dir = rover.getDirection()

	storage.messagesOut.put(f"S,DIR,{dir}")

	return

def moveToAngle (cmd, rover):

	try:

		angle = float(cmd[2])

		print("Angle:")
		print(angle)
		print()

		try:

			rad = bool(cmd[3])

			rover.moveToAngle(angle, rad)

			return

		except:

			rover.moveToAngle(angle)

			return

	except:

		storage.messagesOut.put("E,Angle Must Be Provided")

		return