import board
import storage
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag

def main ():

	with open(simFile, 'a') as f:

		f.write(f"Time,MagX,MagY,MagZ,AccX,AccY,AccZ\n")

	simFile = f"sim/{datetime.datetime.utcnow().timestamp()}.sim"

	i2c = board.I2C()
	mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
	accel = adafruit_lsm303_accel.LSM303_Accel(i2c)

	while True:

		magRead = mag.magnetic
		accelRead = accel.acceleration

		magX = magRead.x
		magY = magRead.y
		magZ = magRead.z

		accX = accelRead.x
		accY = accelRead.y
		accZ = accelRead.z

		with open(simFile, 'a') as f:

			f.write(f"{datetime.datetime.utcnow().timestamp()},{magX},{magY},{magZ},{accX},{accY},{accZ}\n")

		if (storage.exiting):

			break