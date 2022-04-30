import time
import math
import numpy as np

#from imageProcessor import getPath
def IRTest(rover):
	if rover.pingIR1() == True:
		print("White")

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

	rover.moveRover("f")

	distance = rover.measureDistance()

	while ( > 25):

		print(distance)

		distance = rover.measureDistance()

		pass

	rover.moveRover("s")

def distanceChallenge (rover, distance):

	rover.moveRover("f", 0.5)
	time.sleep(distance / 28.5)
	rover.moveRover("s")

# assumes that 0 degrees is north
# possibly add if elif else statments to accodmetate for angles over 180 degrees
def directionChallenge (rover, target):

	print("Found Angle")

	if (target > 0):

		rover.moveRover("rr", 0.5)
		time.sleep(target / 200)
		rover.moveRover("f", 0.5)
		time.sleep(3.2)
		rover.moveRover("s")

	else:

		rover.moveRover("rl", 0.5)
		time.sleep(abs(target) / 200)
		rover.moveRover("f", 0.5)
		time.sleep(3.2)
		rover.moveRover("s")

def obstacleAvoidance2 (rover):

	count = 0

	while True:

		direction = rover.getDirection()
		rover.moveRover("f")

		while (rover.measureDistance() > 5):

			pass

		rover.moveRover("cfl")
		rover.moveServo(1)
		timeStart = time.time()

		while (rover.measureDistance() > 10):

			pass

		timeEnd = time.time()
		rover.moveRover("cfr")
		time.sleep(timeEnd - timeStart)
		direction2 = rover.getDirection()

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

		if (count == 1):

			break

def parallelParking (rover, left = False):

	if left:

		rover.moveServo(-1)
		rover.moveRover("l")

	else:

		rover.moveServo(1)
		rover.moveRover("r")

	while (rover.measureDistance() > 3):

		pass

	rover.moveRover("s")

def stayInYourLane (rover):

	while True:

		rover.moveRover("f")

		if rover.pingIR1() == True:

			rover.moveRover("cfr")
			time.sleep(1.5)
			rover.moveRover("cfl")
			time.sleep(1.5)

#def stayInYourLaneTry (rover):

#	while True:

#		rover.moveRover("f", target = 0.25)

#		if (rover.pingIR1()):

#			rover.moveRover("cfr", target = 0.25)
#			rover.moveRover("cfl", target = 0.25)

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
