import time
import board
import storage
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag

import pandas as pd

def main ():

	simFile = f"sim/{storage.now}.sim"

	data = pd.DataFrame(columns = ["Time", "Time Since Start", "MagX", "MagY", "MagZ", "AccX", "AccY", "AccZ"])

	with open(simFile, 'a') as f:

		f.write(f"Time,Time Since Start,MagX,MagY,MagZ,AccX,AccY,AccZ\n")

	i2c = board.I2C()
	mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
	accel = adafruit_lsm303_accel.LSM303_Accel(i2c)

	start = time.time()

	while True:

		magRead = mag.magnetic
		accelRead = accel.acceleration

		data.loc[len(data)] = [time.time(), (time.time() - start), magRead[0], magRead[1], magRead[2], accelRead[0], accelRead[1], accelRead[2]]

		if (storage.exiting):

			with open(simFile, 'a') as f:

				for index, i in data.iterrows():

					f.write(f"{i['Time']},{i['Time Since Start']},{i['MagX']},{i['MagY']},{i['MagZ']},{i['AccX']},{i['AccY']},{i['AccZ']}\n")

			break