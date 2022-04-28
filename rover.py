import queue
import storage

import numpy as np

from time import sleep, time, strftime
from distanceFinder import findDistanceTraveled

class motors:

	def __init__ (self, defaultThrottle = 100):

		self.__testing = False

		if (storage.testing):

			self.__testing = True

		else:

			from PCA9685 import PCA9685

			# Motor Layout
			# B ----- A
			#     |
			#     |
			# D ----- C

			# Variables for Motors A and B (Front two wheels)
			self.PWMA = 0
			self.ANeg = 1
			self.APos = 2
			self.BNeg = 3
			self.BPos = 4
			self.PWMB = 5

			# Variables for Motors C and D (Back two wheels)
			self.PWMC = 0
			self.CNeg = 1
			self.CPos = 2
			self.DNeg = 3
			self.DPos = 4
			self.PWMD = 5

			# Creates Wheel Pair Variables

			self.__frontWheels = PCA9685(0x40, debug = False)
			self.__backWheels = PCA9685(0x44, debug = False)

			self.__frontWheels.setPWMFreq(1000)
			self.__backWheels.setPWMFreq(1000)

	def forwards (self, wheel, speed):

		for i in wheel:

			if (i == "A"):

				self.__frontWheels.setDutycycle(self.PWMA, speed)

				self.__frontWheels.setLevel(self.ANeg, 0)
				self.__frontWheels.setLevel(self.APos, 1)

			elif (i == "B"):

				self.__frontWheels.setDutycycle(self.PWMB, speed)

				self.__frontWheels.setLevel(self.BNeg, 0)
				self.__frontWheels.setLevel(self.BPos, 1)

			elif (i == "C"):

				self.__backWheels.setDutycycle(self.PWMC, speed)

				self.__backWheels.setLevel(self.CNeg, 0)
				self.__backWheels.setLevel(self.CPos, 1)

			elif (i == "D"):

				self.__backWheels.setDutycycle(self.PWMD, speed)

				self.__backWheels.setLevel(self.DNeg, 0)
				self.__backWheels.setLevel(self.DPos, 1)

	def backwards (self, wheel, speed):

		for i in wheel:

			if (i == "A"):

				self.__frontWheels.setDutycycle(self.PWMA, speed)

				self.__frontWheels.setLevel(self.ANeg, 1)
				self.__frontWheels.setLevel(self.APos, 0)

			elif (i == "B"):

				self.__frontWheels.setDutycycle(self.PWMB, speed)

				self.__frontWheels.setLevel(self.BNeg, 1)
				self.__frontWheels.setLevel(self.BPos, 0)

			elif (i == "C"):

				self.__backWheels.setDutycycle(self.PWMC, speed)

				self.__backWheels.setLevel(self.CNeg, 1)
				self.__backWheels.setLevel(self.CPos, 0)

			elif (i == "D"):

				self.__backWheels.setDutycycle(self.PWMD, speed)

				self.__backWheels.setLevel(self.DNeg, 1)
				self.__backWheels.setLevel(self.DPos, 0)

	def stop (self, wheel):

		for i in wheel:

			if (i == "A"):

				self.__frontWheels.setDutycycle(self.PWMA, 0)

			elif (i == "B"):

				self.__frontWheels.setDutycycle(self.PWMB, 0)

			elif (i == "C"):

				self.__backWheels.setDutycycle(self.PWMC, 0)

			elif (i == "D"):

				self.__backWheels.setDutycycle(self.PWMD, 0)

	def stopAll (self):

		self.stop(["A", "B", "C", "D"])

	def move (self, movementOption, ratio, speed):

		if (self.__testing):

			print(f"Move: {movementOption}, Ratio: {ratio}, Speed: {speed}")

		else:

			if (movementOption == "f"):

				self.forwards(["A", "B", "C", "D"], speed)

			elif (movementOption == "b"):

				self.backwards(["A", "B", "C", "D"], speed)

			elif (movementOption == "r"):

				self.forwards(["B", "C"], speed)
				self.backwards(["A", "D"], speed)

			elif (movementOption == "l"):

				self.forwards(["A", "D"], speed)
				self.backwards(["B", "C"], speed)

			elif (movementOption == "dfr"):

				self.forwards(["B", "C"], speed)
				self.stop(["A", "D"], speed)

			elif (movementOption == "dfl"):

				self.forwards(["A", "D"], speed)
				self.stop(["B", "C"], speed)

			elif (movementOption == "dbr"):

				self.backwards(["A", "D"], speed)
				self.stop(["B", "C"], speed)

			elif (movementOption == "dbl"):

				self.backwards(["B", "C"], speed)
				self.stop(["A", "D"], speed)

			elif (movementOption == "cfr"):

				self.forwards(["B", "D"], speed)
				self.forwards(["A", "C"], (speed * ratio))

			elif (movementOption == "cfl"):

				self.forwards(["A", "C"], speed)
				self.forwards(["B", "D"], (speed * ratio))

			elif (movementOption == "cbr"):

				self.backwards(["B", "D"], speed)
				self.backwards(["A", "C"], (speed * ratio))

			elif (movementOption == "cbl"):

				self.backwards(["A", "C"], speed)
				self.backwards(["B", "D"], (speed * ratio))

			elif (movementOption == "rr"):

				self.forwards(["B", "D"], speed)
				self.backwards(["A", "C"], speed)

			elif (movementOption == "rl"):

				self.forwards(["A", "C"], speed)
				self.backwards(["B", "D"], speed)

			elif (movementOption == "s"):

				self.stopAll()

class rover:

	def __init__ (self, camera = True, magAndAccel = True, servo = True, ultraSonic = True, defaultThrottle = 100, servoPin = 17):

		self.__i2c = None
		self.__mag = None
		self.__accel = None
		self.__servo = None
		self.__motors = None
		self.__camera = None
		self.__timeOfFlight = None

		self.__limit = 90
		#self.__correction = -0.15
		#self.__servo_correction = -0.23

		#self.__minPW = (1.0 - self.__correction) / 1000
		#self.__maxPW = (2.0 + self.__correction + self.__servo_correction) / 1000

		self.__servoPin = servoPin

		self.__defaultThrottle = defaultThrottle

		self.__cameraNeeded = camera
		self.__maNeeded = magAndAccel
		self.__servoNeeded = servo
		self.__tofNeeded = ultraSonic

		self.__motorError = False
		self.__cameraError = False
		self.__maError = False
		self.__servoError = False
		self.__tofError = False

		self.__testing = False

		self.__distance = 0
		self.__lastVelocity = np.asarray([[0], [0], [0]])
		self.__lastPosition = np.asarray([[0], [0], [0]])

		try:

			self.__motors = motors()

			self.__motorError = False

		except Exception as e:

			print(f"Motor Exception: {e}")

			self.__motorError = True

		if (storage.testing):

			self.__testing = True

		else:

			import board

			if (self.__cameraNeeded):

				try:

					import picamera
					self.__camera = picamera.PiCamera()

					self.__cameraError = False

				except Exception as e:

					print(e)

					self.__cameraError = True

			if (self.__maNeeded):

				try:

					import adafruit_lsm303_accel
					import adafruit_lsm303dlh_mag

					self.__i2c = board.I2C()
					self.__mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(self.__i2c)
					self.__accel = adafruit_lsm303_accel.LSM303_Accel(self.__i2c)

					self.__maError = False

				except Exception as e:

					self.__maError = True

			if (self.__servoNeeded):

				from gpiozero import AngularServo

				try:

					self.__servo = AngularServo(self.__servoPin, min_angle = (-1 * self.__limit), max_angle = self.__limit)

					self.__servoError = False

				except Exception as e:

					print(e)

					self.__servoError = True

			if (self.__tofNeeded):

				try:

					import adafruit_vl53l1x

					self.__i2c = board.I2C()

					self.__timeOfFlight = adafruit_vl53l1x.VL53L1X(self.__i2c)

					self.__timeOfFlight.distance_mode = 2
					self.__timeOfFlight.timing_budget = 50

					if (self.__timeOfFlight == None):

						self._tofError = False

					else:

						self._tofError = False

				except Exception as e:

					self._tofError = True

			storage.messagesOut.put(f"S,SU,M:True:{self.__motorError},C:{self.__cameraNeeded}:{self.__cameraError},A:{self.__maNeeded}:{self.__maError},S:{self.__servoNeeded}:{self.__servoError},T:{self.__tofNeeded}:{self.__tofError}")

			storage.status = [["M", True, self.__motorError], ["C", self.__cameraNeeded, self.__cameraError], ["A", self.__maNeeded, self.__maError], ["S", self.__servoNeeded, self.__servoError], ["T", self.__tofNeeded, self._tofError]]

	def statusUpdate (self):

		if (self.__testing):

			print("Status Update")

		else:

			storage.messagesOut.put(f"S,SU,M:True:{self.__motorError},C:{self.__cameraNeeded}:{self.__cameraError},A:{self.__maNeeded}:{self.__maError},S:{self.__servoNeeded}:{self.__servoError},T:{self.__tofNeeded}:{self.__tofError}")

			storage.status = [["M", True, self.__motorError], ["C", self.__cameraNeeded, self.__cameraError], ["A", self.__maNeeded, self.__maError], ["S", self.__servoNeeded, self.__servoError], ["T", self.__tofNeeded, self.__tofError]]

			return

	def measureDistance (self, cm = False):

		if (self.__testing):

			print("Measure Distance")

		else:

			while True:

				try:

					self.__timeOfFlight.start_ranging()

					while True:

						if (self.__timeOfFlight.data_ready):

							distance = self.__timeOfFlight.distance

							self.__timeOfFlight.clear_interrupt()

							break

					self.__timeOfFlight.stop_ranging()

					break

				except:

					print("Error")

					pass

			if (cm):

				return distance

			else:

				return (distance / (2.54))

	# TODO: Needs implimentation
	def moveDistance (self, distance, cm = False, report = False):

		if (self.__testing):

			print("Move Distance")

		else:

			current = time()

			self.moveRover("f", 0.23)

			while (True):

				state = findDistanceTraveled((time() - current), self.getMag(), self.getAccel(), self.__lastVelocity, self.__lastPosition)

				self.__distance += state[0]
				self.__lastVelocity = state[1]
				self.__lastPosition = state[2]

				if (cm):

					if (report):

						storage.messagesOut.put(f"S,D,{state[0]}cm")

					if (distance <= self.__distance):

						self.moveRover("s")

						self.__distance = 0
						self.__lastVelocity = np.asarray([[0], [0], [0]])
						self.__lastPosition = np.asarray([[0], [0], [0]])

						break

				else:

					if (report):

						storage.messagesOut.put(f"S,D,{state[0] / 2.54}in")

					if (distance <= (state[0] / 2.54)):

						self.moveRover("s")

						self.__lastVelocity = np.asarray([[0], [0], [0]])
						self.__lastPosition = np.asarray([[0], [0], [0]])

						break

				current = time()

	def moveToAngle (self, angle):

		if (self.__testing):

			print("Move Angle")

		else:

			try:

				direction = self.getDirection(True)
				lowerLimit = 0.23
				angleDesired = np.round(angle, 0) * (np.pi / 180)

				print("Starting Vals:")
				print(f"Direction: {(direction * (180 / np.pi))}, Desired: {(angleDesired * (180 / np.pi))}, Lower Limit: {lowerLimit}")
				print()

				if (np.cross(np.array([np.cos(direction), np.sin(direction)]), np.array([np.cos(angleDesired), np.sin(angleDesired)])) > 0):

					self.moveRover("cfl", throttle = 1)
					print("Move Left")

				else:

					self.moveRover("cfr", throttle = 1)
					print("Move Right")

				print()

				while (True):

					angleFound = self.getDirection() * (np.pi / 180)

					diff = np.abs(np.round((angleDesired * (180 / np.pi)), 0) - np.round((angleFound * (180 / np.pi)), 0))

					print(f"Diff: {diff}")

					speed = lowerLimit

					if (speed > 1):

						speed = 1

					if (diff <= 10):

						speed = lowerLimit

					print(f"At angle: {np.round((angleFound * (180 / np.pi)), 0)}, looking for: {np.round((angleDesired * (180 / np.pi)), 0)}")

					print(np.cross(np.array([np.cos(angleFound), np.sin(angleFound)]), np.array([np.cos(angleDesired), np.sin(angleDesired)])))

					if (diff == 0):

						self.moveRover("s")

						break

					elif (np.cross(np.array([np.cos(angleFound), np.sin(angleFound)]), np.array([np.cos(angleDesired), np.sin(angleDesired)])) > 0):

						self.moveRover("cfl", throttle = speed)
						print("Move Left")

					else:

						self.moveRover("cfr", throttle = speed)
						print("Move Right")

					print()

			except Exception as e:

				print(e)

	def moveRover (self, movementOption, percent = 0.5, throttle = None):

		if (throttle == None):

			throttle = self.__defaultThrottle

		else:

			throttle = self.__defaultThrottle * throttle

		self.__motors.move(movementOption, ratio = percent, speed = throttle)

	def moveServo (self, servoAngle):

		if (self.__testing):

			print("Move Servo")

		else:

			#if (servoAngle < 0):

				#self.__servo.value = (servoAngle - (self.__servo_correction / 2))

			#elif (servoAngle > 0):

				#self.__servo.value = (servoAngle + (self.__servo_correction / 2))

			#else:

				#self.__servo.value = (0 + self.__servo_correction)

			self.__servo.value = servoAngle

	def getAccel (self):

		if (self.__testing):

			print("Get Accel")

		else:

			return self.__accel.acceleration

	def getAvrDistance (self, numPulses = 5):

		if (self.__testing):

			print("Get Average Distance")

		else:

			totalDistance = 0

			for i in range(numPulses):

				totalDistance += self.measureDistance()

			return (totalDistance / numPulses)

	def getDistance (self):

		if (self.__testing):

			print("Get Distance")

		else:

			return self.measureDistance()

	def getMag (self):

		if (self.__testing):

			print("Get Mag")

		else:

			return self.__mag.magnetic

	def getDirection (self, rad = False):

		if (self.__testing):

			print("Get Direction")

		else:

			mag = self.getMag()
			accel = self.getAccel()

			roll = np.arctan2(accel[1], np.sqrt(np.power(accel[0], 2) + np.power(accel[2], 2)))
			pitch = np.arctan2(accel[0], np.sqrt(np.power(accel[1], 2) + np.power(accel[2], 2)))

			magX = (mag[0] * np.cos(pitch)) + (mag[1] * np.sin(roll) * np.sin(pitch)) + (mag[2] * np.cos(roll) * np.sin(pitch))
			magY = (mag[1] * np.cos(roll)) - (mag[2] * np.sin(roll))
			yaw = np.arctan2((-1 * magY), magX)

			yawCorrected = ((2 * np.pi) + yaw) % (2 * np.pi)

			if (rad):

				return yawCorrected

			return np.degrees(yawCorrected)

	def takePic (self):

		if (self.__testing):

			print("Take Picture")

		else:

			self.__camera.start_preview()
			sleep(2)

			date_string = strftime("%Y-%m-%d-%H:%M")

			self.__camera.capture(f"/home/pi/Raspberry-Pi/images/{date_string}.png")
			self.__camera.stop_preview()

			storage.messagesOut.put("file")
			storage.messagesOut.put(f"/home/pi/Raspberry-Pi/images/{date_string}.png")

	def redoMotors (self):

		if (self.__testing):

			print("Redo Motors")

		else:

			try:

				self.__motors = motors()

			except:

				storage.messagesOut.put("S,Motors not online ... Check connection")

				self.__motorError = True

			storage.messagesOut.put(f"S,SU,M:True:{self.__motorError},C:{self.__cameraNeeded}:{self.__cameraError},A:{self.__maNeeded}:{self.__maError},S:{self.__servoNeeded}:{self.__servoError},T:{self.__tofNeeded}:{self.__tofError}")

	def redoCamera (self):

		if (self.__testing):

			print("Redo Cam")

		else:

			try:

				self.__cameraNeeded = True

				self.__camera = PiCamera()

			except:

				storage.messagesOut.put("S,Camera not online ... Check connection")

				self.__cameraError = True

			storage.messagesOut.put(f"S,SU,M:True:{self.__motorError},C:{self.__cameraNeeded}:{self.__cameraError},A:{self.__maNeeded}:{self.__maError},S:{self.__servoNeeded}:{self.__servoError},T:{self.__tofNeeded}:{self.__tofError}")

	def redoMagAndAccel (self):

		if (self.__testing):

			print("Redo MA")

		else:

			try:

				self.__maNeeded = True

				self.__i2c = board.I2C()
				self.__mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(self.__i2c)
				self.__accel = adafruit_lsm303_accel.LSM303_Accel(self.__i2c)

			except:

				storage.messagesOut.put("S,Magnetometer and accelerometer not online ... Check connection")

				self.__maError = True

			storage.messagesOut.put(f"S,SU,M:True:{self.__motorError},C:{self.__cameraNeeded}:{self.__cameraError},A:{self.__maNeeded}:{self.__maError},S:{self.__servoNeeded}:{self.__servoError},T:{self.__tofNeeded}:{self.__tofError}")

	def redoServo (self):

		if (self.__testing):

			print("Redo Servo")

		else:

			try:

				self.__servoNeeded = True

				self.__servo = Servo(self.__servoPin, min_pulse_width = self.__minPW, max_pulse_width = self.__maxPW)

			except:

				storage.messagesOut.put("S,Servo not online ... Check connection")

				self.__servoError = True

			storage.messagesOut.put(f"S,SU,M:True:{self.__motorError},C:{self.__cameraNeeded}:{self.__cameraError},A:{self.__maNeeded}:{self.__maError},S:{self.__servoNeeded}:{self.__servoError},T:{self.__tofNeeded}:{self.__tofError}")


	def redoTimeOfFlight (self):

		if (self.__testing):

			print("Redo ToF")

		else:

			try:

				import adafruit_vl53l1x

				self.__tofNeeded = True

				i2c = board.I2C()

				self.__timeOfFlight = adafruit_vl53l1x.VL53L1X(i2c)

				self.__timeOfFlight.distance_mode = 1
				self.__timeOfFlight.timing_budget = 100

				self.__timeOfFlight.start_ranging()

				self._tofError = False

			except Exception as e:

				storage.messagesOut.put("S,Time of Flight Sensor not online ... Check connection")


				self.__tofError = True

			storage.messagesOut.put(f"S,SU,M:True:{self.__motorError},C:{self.__cameraNeeded}:{self.__cameraError},A:{self.__maNeeded}:{self.__maError},S:{self.__servoNeeded}:{self.__servoError},T:{self.__tofNeeded}:{self.__tofError}")
