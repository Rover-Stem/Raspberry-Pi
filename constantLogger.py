import board
import storage
import datetime
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag

def main ():

	simFile = f"sim/{datetime.datetime.utcnow().timestamp()}.sim"

	with open(simFile, 'a') as f:

		f.write(f"Time,MagX,MagY,MagZ,AccX,AccY,AccZ\n")

	i2c = board.I2C()
	mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
	accel = adafruit_lsm303_accel.LSM303_Accel(i2c)

	while True:

		magRead = mag.magnetic
		accelRead = accel.acceleration

		magX = magRead[0]
		magY = magRead[1]
		magZ = magRead[2]

		accX = accelRead[0]
		accY = accelRead[1]
		accZ = accelRead[2]

		with open(simFile, 'a') as f:

			f.write(f"{datetime.datetime.utcnow().timestamp()},{magX},{magY},{magZ},{accX},{accY},{accZ}\n")

		if (storage.exiting):

			break