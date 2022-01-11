import board
import queue
import storage

import RPi.GPIO as GPIO

from time import sleep, time, strftime
from PCA9685 import PCA9685

class motors:

	def __init__ (self, defaultThrottle = 100):

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

		self.__frontWheels.setPWMFreq(50)
		self.__backWheels.setPWMFreq(50)

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

		if (movementOption == "f"):

			self.forwards(["A", "B", "C", "D"], speed)

		elif (movementOption == "b"):

			self.backwards(["A", "B", "C", "D"], speed)

		elif (movementOption == "r"):

			speed = speed

			self.forwards(["B", "C"], speed)
			self.backwards(["A", "D"], speed)

		elif (movementOption == "l"):

			speed = speed

			self.forwards(["A", "D"], speed)
			self.backwards(["B", "C"], speed)

		elif (movementOption == "dfr"):

			self.forwards(["B", "C"], speed)

		elif (movementOption == "dfl"):

			self.forwards(["A", "D"], speed)

		elif (movementOption == "dbr"):

			self.backwards(["A", "D"], speed)

		elif (movementOption == "dbl"):

			self.backwards(["B", "C"], speed)

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

	def __init__ (self, camera = True, magAndAccel = True, servo = True, ultraSonic = True, defaultThrottle = 100, servoPin = 22, echoPin = 24, triggerPin = 23):

		self.__i2c = None
		self.__mag = None
		self.__accel = None
		self.__servo = None
		self.__motors = None
		self.__camera = None
		self.__ultra_sonic = None

		self.__correction = -0.15
		self.__servo_correction = -0.23
		self.__minPW = (1.0 - self.__correction) / 1000
		self.__maxPW = (2.0 + self.__correction + self.__servo_correction) / 1000

		self.__echoPin = echoPin
		self.__servoPin = servoPin
		self.__triggerPin = triggerPin

		self.__defaultThrottle = defaultThrottle

		self.__cameraNeeded = camera
		self.__maNeeded = magAndAccel
		self.__servoNeeded = servo
		self.__usNeeded = ultraSonic

		self.__motorError = False
		self.__cameraError = False
		self.__maError = False
		self.__servoError = False
		self.__usError = False

		try:

			self.__motors = motors()

		except Exception as e:

			storage.messagesOut.put("Motors not online ... Check connection")


			self.__motorError = True

		if (self.__cameraNeeded):

			try:

				import picamera
				self.__camera = picamera.PiCamera()

			except Exception as e:

				storage.messagesOut.put("Camera not online ... Check connection")


				self.__cameraError = True

		if (self.__maNeeded):

			try:

				import adafruit_lsm303_accel
				import adafruit_lsm303dlh_mag

				self.__i2c = board.I2C()
				self.__mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(self.__i2c)
				self.__accel = adafruit_lsm303_accel.LSM303_Accel(self.__i2c)

			except Exception as e:

				storage.messagesOut.put("Magnetometer and accelerometer not online ... Check connection")


				self.__maError = True

		if (self.__servoNeeded):

			from gpiozero import Servo

			try:

				self.__servo = Servo(self.__servoPin, min_pulse_width = self.__minPW, max_pulse_width = self.__maxPW)

			except Exception as e:

				storage.messagesOut.put("Servo not online ... Check connection")


				self.__servoError = True

		if (self.__usNeeded):

			try:

				GPIO.setmode(GPIO.BCM)
				GPIO.setup(self.__echoPin, GPIO.IN)
				GPIO.setup(self.__triggerPin, GPIO.OUT)

				GPIO.output(self.__triggerPin, False)

				sleep(2)

			except Exception as e:

				storage.messagesOut.put("Ultrasonic not online ... Check connection")


				self.__usError = True

		storage.messagesOut.put(f"S,SU,M:True:{self.__motorError},C:{self.__cameraNeeded}:{self.__cameraError},A:{self.__maNeeded}:{self.__maError},S:{self.__servoNeeded}:{self.__servoError},U:{self.__usNeeded}:{self.__usError}")

	def measureDistance (self):

		GPIO.output(self.__triggerPin, GPIO.HIGH)

		sleep(0.00001)

		GPIO.output(self.__triggerPin, GPIO.LOW)

		while (GPIO.input(self.__echoPin) == 0):

  			pulse_start = time()

		while (GPIO.input(self.__echoPin) == 1):

  			pulse_end = time()

		pulse_duration = pulse_end - pulse_start

		distance = pulse_duration * 17150

		distance = round(distance, 2

		return distance

	# TODO: Needs implimentation
	def moveDistance (self, distance, cm = False):

		pass

	def moveRover (self, movementOption, percent = 0.5, throttle = None):

		if (throttle == None):

			throttle = self.__defaultThrottle

		self.__motors.move(movementOption, ratio = percent, speed = throttle)

	def moveServo (self, servoAngle):

		if (servoAngle < 0):

			self.__servo.value = (servoAngle - (self.__servo_correction / 2))

		elif (servoAngle > 0):

			self.__servo.value = (servoAngle + (self.__servo_correction / 2))

		else:

			self.__servo.value = (0 + self.__servo_correction)

	def getAccel (self):

		return self.__accel.acceleration

	def getAvrDistance (self, pulse_wait = 0.0001, numPulses = 5):

		totalDistance = 0

		for i in range(numPulses):

			totalDistance += self.measureDistance()

			sleep(pulse_wait)

		return (totalDistance / numPulses)

	def getDistance (self):

		return self.measureDistance()

	def getMag (self):

		return self.__mag.magnetic

	def takePic (self):

		self.__camera.start_preview()
		sleep(2)

		date_string = strftime("%Y-%m-%d-%H:%M")

		self.__camera.capture(f"/home/pi/Raspberry-Pi/images/{date_string}.png")
		self.__camera.stop_preview()

	def redoMotors (self):

		try:

			self.__motors = motors()

		except:

			storage.messagesOut.put("Motors not online ... Check connection")

			self.__motorError = True

		storage.messagesOut.put(f"S,SU,M:True:{self.__motorError},C:{self.__cameraNeeded}:{self.__cameraError},A:{self.__maNeeded}:{self.__maError},S:{self.__servoNeeded}:{self.__servoError},U:{self.__usNeeded}:{self.__usError}")

	def redoCamera (self):

		try:

			self.__cameraNeeded = True

			self.__camera = PiCamera()

		except:

			storage.messagesOut.put("Camera not online ... Check connection")

			self.__cameraError = True

		storage.messagesOut.put(f"S,SU,M:True:{self.__motorError},C:{self.__cameraNeeded}:{self.__cameraError},A:{self.__maNeeded}:{self.__maError},S:{self.__servoNeeded}:{self.__servoError},U:{self.__usNeeded}:{self.__usError}")

	def redoMagAndAccel (self):

		try:

			self.__maNeeded = True

			self.__i2c = board.I2C()
			self.__mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(self.__i2c)
			self.__accel = adafruit_lsm303_accel.LSM303_Accel(self.__i2c)

		except:

			storage.messagesOut.put("Magnetometer and accelerometer not online ... Check connection")

			self.__maError = True

		storage.messagesOut.put(f"S,SU,M:True:{self.__motorError},C:{self.__cameraNeeded}:{self.__cameraError},A:{self.__maNeeded}:{self.__maError},S:{self.__servoNeeded}:{self.__servoError},U:{self.__usNeeded}:{self.__usError}")

	def redoServo (self):

		try:

			self.__servoNeeded = True

			self.__servo = Servo(self.__servoPin, min_pulse_width = self.__minPW, max_pulse_width = self.__maxPW)

		except:

			storage.messagesOut.put("Servo not online ... Check connection")

			self.__servoError = True

		storage.messagesOut.put(f"S,SU,M:True:{self.__motorError},C:{self.__cameraNeeded}:{self.__cameraError},A:{self.__maNeeded}:{self.__maError},S:{self.__servoNeeded}:{self.__servoError},U:{self.__usNeeded}:{self.__usError}")


	def redoUltraSonic (self):

		try:

			self.__ultra_sonic = adafruit_hcsr04.HCSR04(trigger_pin = board.D5, echo_pin = board.D6)
			self.__ultra_sonic.distance

		except Exception as e:

			storage.messagesOut.put("Ultrasonic not online ... Check connection")


			self.__usError = True

		storage.messagesOut.put(f"S,SU,M:True:{self.__motorError},C:{self.__cameraNeeded}:{self.__cameraError},A:{self.__maNeeded}:{self.__maError},S:{self.__servoNeeded}:{self.__servoError},U:{self.__usNeeded}:{self.__usError}")