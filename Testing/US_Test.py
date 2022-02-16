from gpio import DistanceSensor

echoPin = 24
triggerPin = 23

us = DistanceSensor(24, 23)

for i in range(30):

	print(f"Distance: {us.distance * 100}")