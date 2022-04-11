import time

import numpy as np

from imageProcessor import getPath

def square (rover):

	for i in range(4):

		rover.moveRover("f")
		time.sleep(1)
		rover.moveRover("s")

		rover.moveRover("rr")
		time.sleep(1)
		rover.moveRover("s")

def obstacleAvoidance1 (rover):

	rover.moveRover("f")

	while (rover.measureDistance() > 25):
		pass

	rover.moveRover("s")

def distanceChallenge (rover, distance):

	rover.moveDistance(distance)
	
# assumes that getDirection returns is oriented with the Unit Circle
def directionChallenge (rover, start, target):
	direction = start
	targetDirection = target
	while True:
		if direction > targetDirection:
			rover.moveRover("cfr")
		elif direction < targetDirection:
			rover.moveRover("cfl")
		else:
			rover.moveRover("f")
		direction = rover.getDirection()


def obstacleAvoidance2 (rover, numObstacles):

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
		rover.moveRover("l")

	else:

		rover.moveServo(1)
		rover.moveRover("r")

	while (rover.measureDistance() > 3):

		pass

	rover.moveRover("s")

def stayInYourLane (rover):

	while True:

		diff = np.round(getPath(), 1)

		if (diff == 0):

			pass

		elif (diff < 0):

			rover.moveRover("cfr")

		elif (diff > 0):

			rover.moveRover("cfl")

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
