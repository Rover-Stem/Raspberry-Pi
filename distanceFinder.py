import numpy as np
import pandas as pd

def rotX (vector, rads):

	rot = np.asarray([[1, 0, 0], [0, np.cos(rads), (-1 * np.sin(rads))], [0, np.sin(rads), np.cos(rads)]])
	return rot.dot(vector)

def rotY (vector, rads):

	rot = np.asarray([[np.cos(rads), 0, np.sin(rads)], [0, 1, 0], [(-1 * np.sin(rads)), 0, np.cos(rads)]])
	return rot.dot(vector)

def rotZ (vector, rads):

	rot = np.asarray([[np.cos(rads), (-1 * np.sin(rads)), 0], [np.sin(rads), np.cos(rads), 0], [0, 0, 1]])
	return rot.dot(vector)

def findHeading (vector, roll, pitch):

	magX = (vector[0] * np.cos(pitch)) + (vector[1] * np.sin(roll) * np.sin(pitch)) + (vector[2] * np.cos(roll) * np.sin(pitch))
	magY = (vector[1] * np.cos(roll)) - (vector[2] * np.sin(roll))
	yaw = np.arctan2((-1 * magY), magX)

	yawCorrected = (np.pi + yaw) % np.pi

	return heading

def findPitch (vector):

	return np.arctan2(vector[0], np.sqrt(np.power(vector[1], 2) + np.power(vector[2], 2)))

def findRoll (vector):

	return np.arctan2(vector[1], np.sqrt(np.power(vector[0], 2) + np.power(vector[2], 2)))

def findVelocity (vector, pitch, roll, yaw, dt):

	# Correct Vector

	vectCorrX = rotX(vector, (-1 * roll))
	vectCorrY = rotY(vectCorrX, (-1 * pitch))
	vectCorrZ = rotZ(vectCorrY, (-1 * yaw))
	vectCorrZ = np.asarray([vectCorrZ[0], vectCorrZ[1], 0])

	return vectCorrZ * dt

def correctMag (vector, roll, pitch):

	vectCorrX = rotX(vector, (-1 * roll))
	vectCorrY = rotY(vectCorrX, (-1 * pitch))

	return vectCorrY

def findDistanceTraveled (dt, mag, accel, prevVel, prevPos):

	smoothedMagX = np.convolve(mag[0], np.ones((50, )) / 50, mode = 'same')
	smoothedMagY = np.convolve(mag[1], np.ones((50, )) / 50, mode = 'same')
	smoothedMagZ = np.convolve(mag[2], np.ones((50, )) / 50, mode = 'same')

	smoothedAccX = np.convolve(accel[0], np.ones((50, )) / 50, mode = 'same')
	smoothedAccY = np.convolve(accel[1], np.ones((50, )) / 50, mode = 'same')
	smoothedAccZ = np.convolve(accel[2], np.ones((50, )) / 50, mode = 'same')

	magVec = np.asarray([[smoothedMagX], [smoothedMagY], [smoothedMagZ]])
	accVec = np.asarray([[smoothedAccX], [smoothedAccY], [smoothedAccZ]])

	roll = findRoll(accVec)
	pitch = findPitch(accVec)

	velocity = prevVel + findVelocity(accVec, pitch, roll, findHeading(correctMag(magVec, roll, pitch), roll, pitch), dt)
	position = prevPos + (velocity * dt)

	return [(np.sqrt(position.dot(position)) * 100), velocity, position]
