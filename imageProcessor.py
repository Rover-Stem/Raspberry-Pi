import cv2
import sys
import time

import numpy as np
import matplotlib.pyplot as plt

def findAllLines (points):

	lines = []
	itemsToPop = []
	lineBuilder = []
	pointsCopy = points
	lastLineFinished = True

	while len(pointsCopy) > 0:

		lineBuilder.append(pointsCopy.pop(0))

		for i in range(len(pointsCopy)):

			if (np.sqrt(np.power(lineBuilder[-1][0] - pointsCopy[i][0], 2) + np.power(lineBuilder[-1][1] - pointsCopy[i][1], 2)) <= 20):

				lineBuilder.append(pointsCopy[i])
				itemsToPop.append(i)

		for i in range((len(itemsToPop) - 1), -1, -1):

			pointsCopy.pop(itemsToPop[i])

		lines.append(lineBuilder)

		lineBuilder = []
		itemsToPop = []

	return lines

def difference (arr, y, thresholdImage):

	binSize = 40
	binStart = 280

	arr2 = arr
	diffArr = []

	arr2.sort()

	#print("XVals")
	#print(xVals)
	#print()

	for i in range(len(arr2) - 1):

		if not(thresholdImage[y, int((arr2[i + 1] + arr2[i]) / 2)] == 255):

			continue

		difference = (arr2[i + 1] - arr2[i])

		if ((difference > binStart) and (difference < (binSize + binStart))):

			diffArr.append([difference, [arr2[i], arr2[i + 1]]])

	#print("Diffs")
	#print([diff[0] for diff in diffArr])
	#print()

	return diffArr

def getPath (imgPath):

	paths = False
	images = False
	graphing = False

	np.set_printoptions(threshold = sys.maxsize)

	#tStart = time.time()

	img = np.flip(np.flipud(cv2.imread(imgPath)), axis = 0).copy()

	origDims = img.shape

	img = img[0:int(img.shape[0] * (5 / 8))]

	imgCopy = img.copy()

	if (images):

		plt.imshow(img)
		plt.show()

	imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	imgFiltered = cv2.boxFilter(imgHSV[:, :, 2].astype(int), -1, (50, 50), normalize = False)

	imgValueScaled = (imgFiltered * (255 / np.max(imgFiltered))).astype(np.uint8)

	imgOutVal = cv2.inRange(imgValueScaled, 72, 160)

	if (images):

		plt.imshow(imgOutVal)
		plt.show()

	if (cv2.version == '3.2.0'):

		_, contoursVal, hierarchyVal = cv2.findContours(imgOutVal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	else:

		contoursVal, hierarchyVal = cv2.findContours(imgOutVal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	if (images):

		imgCont = cv2.drawContours(img, contoursVal, -1, (255, 0, 0), 2)

		plt.imshow(imgCont)
		plt.show()

	else:

		imgCont = img

	normalizedCont = []

	for i in contoursVal:

		normalizedCont += i.tolist()

	normalizedCont = list(map(lambda x: x.tolist(), np.split(np.array(normalizedCont).ravel(), len(normalizedCont))))

	dotsToDraw = []
	differeceToPlot = []

	for i in range(1, (img.shape[0] - 1), 10):

		coords = [x[0] for x in normalizedCont if x[1] == i]

		diffs = difference(coords, i, imgOutVal)

		differeceToPlot.append([i, diffs])

		dotsToDraw += [[int((x[1][0] + x[1][1]) / 2), i] for x in diffs]

	# if (graphing):
	#
	# 	fig = plt.figure()
	#
	# 	ax = fig.add_subplot(2, 2, 1)
	#
	# 	binSize = 100
	#
	# 	ax.title.set_text(f"Frequency - Bins of {binSize}")
	#
	# 	differences = []
	#
	# 	for y, x in differeceToPlot:
	#
	# 		diffs = [z[0] for z in x]
	#
	# 		for i in diffs:
	#
	# 			differences.append(i)
	#
	# 	ax.hist(differences, bins = range(0, max(differences), binSize), density = True)
	#
	# 	ax.set_xlabel('Difference Vals')
	# 	ax.set_ylabel('Frequency')
	#
	# 	ax = fig.add_subplot(2, 2, 2)
	#
	# 	binSize = 50
	#
	# 	ax.title.set_text(f"Frequency - Bins of {binSize}")
	#
	# 	differences = []
	#
	# 	for y, x in differeceToPlot:
	#
	# 		diffs = [z[0] for z in x]
	#
	# 		for i in diffs:
	#
	# 			differences.append(i)
	#
	# 	ax.hist(differences, bins = range(0, max(differences), binSize), density = True)
	#
	# 	ax.set_xlabel('Difference Vals')
	# 	ax.set_ylabel('Frequency')
	#
	# 	ax = fig.add_subplot(2, 2, 3)
	#
	# 	binSize = 25
	#
	# 	ax.title.set_text(f"Frequency - Bins of {binSize}")
	#
	# 	differences = []
	#
	# 	for y, x in differeceToPlot:
	#
	# 		diffs = [z[0] for z in x]
	#
	# 		for i in diffs:
	#
	# 			differences.append(i)
	#
	# 	ax.hist(differences, bins = range(0, max(differences), binSize), density = True)
	#
	# 	ax.set_xlabel('Difference Vals')
	# 	ax.set_ylabel('Frequency')
	#
	# 	ax = fig.add_subplot(2, 2, 4, projection = "3d")
	#
	# 	for y, x in differeceToPlot:
	#
	# 		#print(f"Y: {y}")
	# 		#print(f"X: {[((xe[1][0] + xe[1][1]) / 2) for xe in x]}")
	# 		#print(f"Diffs: {[z[0] for z in x]}")
	# 		#print()
	#
	# 			ax.scatter3D([z[0] for z in x], [((xe[1][0] + xe[1][1]) / 2) for xe in x], [y] * len(x))
	#
	# 	ax.title.set_text("Scatter Plot")
	# 	ax.set_xlabel('Difference')
	# 	ax.set_ylabel('X-Values')
	# 	ax.set_zlabel('Y-Values', rotation = 45)
	# 	ax.invert_zaxis()
	#
	# 	imgCopy = imgCopy.astype('float32') / 255
	#
	# 	y, z = np.ogrid[0:imgCopy.shape[1], 0:imgCopy.shape[0]]
	#
	# 	ax.plot_surface(-100, y, z, rstride = 5, cstride = 5, facecolors = np.flip(np.rot90(imgCopy), axis = 0))
	#
	# 	fig.tight_layout()
	#
	# 	plt.show()

	imgDot = imgCont

	if (images or paths):

		for i in dotsToDraw:

			imgDot = cv2.circle(imgDot, i, radius = 5, color = (0, 0, 255), thickness = -1)

	cameraCenter = (int(origDims[1] / 2), int(origDims[0] / 2))

	if (images or paths):

		imgDot = cv2.circle(imgDot, cameraCenter, radius = 20, color = (0, 255, 0), thickness = -1)

		plt.imshow(imgDot)
		plt.show()

	lines = findAllLines(dotsToDraw)

	lineLengths = [len(x) for x in lines]

	linePath = lines[lineLengths.index(max(lineLengths))]

	yVals = [x[1] for x in linePath]
	closestPointOnLine = None

	k = 0

	while True:

		if (cameraCenter[1] + k) in yVals:

			closestPointOnLine = linePath[yVals.index(cameraCenter[1] + k)]
			break

		k += 1

	#tEnd = time.time()

	#print("Point on Line:")
	#print(closestPointOnLine)
	#print()
	#print("Camera Center:")
	#print(cameraCenter)
	#print()

	rl = "O"

	if (cameraCenter[0] > (closestPointOnLine[0] + 50)):

		rl = "R" # Right

	elif (cameraCenter[0] < (closestPointOnLine[0] - 50)):

		rl = "L" # Left

	#print(f"Time to run: {tEnd - tStart}")

	diffToCenter = np.sqrt(np.power((cameraCenter[0] - closestPointOnLine[0]), 2) + np.power((cameraCenter[1] - closestPointOnLine[1]), 2))
	avrSlope = -((linePath[0][1] - linePath[-1][1]) / (linePath[0][0] - linePath[-1][0]))

	# Returns: difference between center and point on line, slope of line based on average slope, and whether it is to the right or left of the line
	return [diffToCenter, avrSlope, rl]