#!/usr/bin/python3

import sys
import os
import time

class color:
	HEADER = '\033[95m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	GREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	END = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


file=sys.stdout

try:
	while True:
		tFile = open('/sys/class/thermal/thermal_zone0/temp')
		temp = float(tFile.read())
		tempC = int(temp/1000)
		if (tempC > 49):
			tempD = str(tempC)
			file.write(color.FAIL + color.BOLD + "\rCPU Temperatur: " +  tempD + "'C" + color.END)
		else:
			tempD = str(tempC)
			file.write("\rCPU Temperatur: " + color.WARNING + tempD + "'C" + color.END)

		file.flush()
		time.sleep(1)

except KeyboardInterrupt:
        print("")
        sys.exit()
