import time

import numpy as np

from imageProcessor import getPath

def square (rover, sideTime = 1):

	for i in range(4):

		rover.moveRover("f")
		time.sleep(sideTime)
		rover.moveRover("s")

		rover.moveToAngle((rover.getDirection() - 90) % 360)

def getDirectionLoop (rover):

	for i in range(20):

		print(rover.getDirection())

		time.sleep(1)

def obstacleAvoidance1 (rover):

	rover.moveServo(0)

	rover.moveRover("f", throttle = 0.5)

	angle = 1

	distance = rover.measureDistance()

	#print(f"Distance: {distance}")

	while (distance > 10):

		#print(f"Angle is {angle}")

		angle += 0.05
		angle = angle % 2

		rover.moveServo(-1 + angle)
		#print(f"Angle should be {-1 + angle}")

		distance = rover.measureDistance()

		#print(f"Distance: {distance}")

		pass

	rover.moveRover("s")

def distanceChallenge (rover, distance):

	rover.moveRover("f", throttle = 1)
	time.sleep((distance / (67)))
	rover.moveRover("s")

# assumes that 0 degrees is north
# possibly add if elif else statments to accodmetate for angles over 180 degrees
def directionChallenge (rover, target):

	direction = rover.getDirection()
	targetDirection = target

	while True:

		if (direction < targetDirection):

			rover.moveRover("cfr")

		elif (direction > targetDirection):

			rover.moveRover("cfl")

		else:

			rover.moveRover("f")

		direction = rover.getDirection()

def obstacleAvoidance2 (rover, numObstacles = 1):

	count = 0
	times = 2

	while True:

		rover.moveServo(0)

		#direction = rover.getDirection(True)
		rover.moveRover("f", throttle = 0.25)

		angle = 1

		while ((rover.measureDistance() > 25) or (rover.measureDistance() < 0)):

			angle += 0.05
			angle = angle % 2

			rover.moveServo(-1 + angle)

			pass

		rover.moveRover("cfl", throttle = 0.5)
		rover.moveServo(-1)
		time.sleep(times)
		timeEnd = time.time()
		rover.moveRover("cfr", throttle = 0.5)
		time.sleep(times + 0.2)
		rover.moveRover("cfr", throttle = 0.5)
		time.sleep(times + 0.3)
		rover.moveRover("cfl", throttle = 0.5)
		time.sleep(times + 0.3)
		#direction2 = rover.getDirection()

		rover.moveRover("s")

		return

		# TODO: Work on fixing logic
		while True:

			cross = np.cross(direction2, direction)

			if (np.round(direction, 1) == np.round(direction2, 1)):

				break

			elif (cross > 0):

				rover.moveRover("cfl")

			elif (cross < 0):

				rover.moveRover("cfr")

		rover.moveRover("f")
		rover.moveServo(0)

		count += 1

		if (count == numObstacles):

			break

def parallelParking (rover, left = False):

	if left:

		rover.moveServo(-1)
		rover.moveRover("l", throttle = 0.75)

	else:

		rover.moveServo(1)
		rover.moveRover("r", throttle = 0.75)

	while (rover.measureDistance(True) > 35):

		pass

	rover.moveRover("s")

def stayInYourLane (rover):

	rover.moveRover("f", throttle = 0.23)

	while True:

		diff = np.round(getPath(), 1)

		if (diff == 0):

			pass

		elif (diff < 0):

			rover.moveRover("cfr", throttle = 0.24)

		elif (diff > 0):

			rover.moveRover("cfl", throttle = 0.24)

# Intersections are binary
# stop = [0,0]
# go forward = [0,1]
# right turn = [1,0]
# left turn = [1,1]
def navNeighborhood (rover):

	map = [["n", "n", "end"],
		   ["ir", "s", "il"],
		   ["sws", "n", "n"],
		   ["ir", "s", "start"]]

	while not(AtEnd):

		break

def obstacleAvoidance2_Strafe (rover, numObstacles):

	count = 0

	while True:

		direction = rover.getDirection()
		rover.moveRover("f")

		while (rover.measureDistance() > 5):

			pass

		rover.moveRover("dfl")
		rover.moveServo(1)
		timeStart = time.time()
# insert time or way to know how long before going straight forwards
# It would be possible to not have it move straight and just go diagnol right forwards
# Needs testing
		rover.moveRover("f")
		while (rover.measureDistance() > 10):

			pass

		timeEnd = time.time()
		rover.moveRover("dfr")
		time.sleep(timeEnd - timeStart)
		direction2 = rover.getDirection()
# code below should still work and be useful
		while True:

			cross = np.cross(direction2, direction)

			if (np.round(direction, 1) == np.round(direction2, 1)):

				break

			elif (cross > 0):

				rover.moveRover("cfl")

			elif (cross < 0):

				rover.moveRover("cfr")

		rover.moveRover("f")
		rover.moveServo(0)

		count += 1

		if (count == numObstacles):

			break

# testing required
# for type use: 0 = unknown/automonous 1 = stop 2 = forward 3 = right 4 = left
# Need code for detecting the end of the lane (camera sensor analysis)
def intersectionTest (rover, type):
	rover.moveRover("f")
	if type == 1:
		rover.moveRover("s")
	elif type == 2:
		rover.moveRover("f")
	elif type == 3:
		rover.moverRover("cfr")
	elif type == 4:
		rover.moveRover("cfl")
	else:
		pass
		# Insert Binary Protocol
