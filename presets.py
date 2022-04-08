import time

def square (rover):

	for i in range(4):

		rover.moveRover("f")
		time.sleep(1)
		rover.moveRover("s")

		rover.moveRover("rr")
		time.sleep(1)
		rover.moveRover("s")
