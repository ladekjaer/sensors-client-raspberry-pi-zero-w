from datetime import datetime
import os
import sys
import requests
import socket
import time
from w1thermsensor import W1ThermSensor

url = os.getenv('URL')
sensors_api_key = os.getenv('SENSORS_API_KEY')
interval = os.getenv('INTERVAL')
hostname = socket.gethostname()

if not url or not sensors_api_key or not interval:
	print('You must supply environment variable URL, INTERVAL and SENSORS_API_KEY')
	sys.exit(1)
else:
	try:
		interval = int(interval)
	except:
		print('Environment variable must of type integer.')
		sys.exit(1)
	print('Reporting sensordata to {} each {} seconds'.format(url, interval))

hdr = {'ACCESS-KEY': sensors_api_key}

def getserial():
	# Extract serial from cpuinfo file
	cpuserial = "0000000000000000"
	try:
		f = open('/proc/cpuinfo','r')
		for line in f:
			if line[0:6]=='Serial':
				cpuserial = line[10:26]
		f.close()
	except:
		cpuserial = "ERROR000000000"
 
	return cpuserial

pi_id = getserial()

def getsensordata():
	sensordata = []

	for sensor in W1ThermSensor.get_available_sensors():
		print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
		now = datetime.now().astimezone().isoformat()
		sensordata.append({
			'timestamp': now,
			'thermostat_id': sensor.id,
			'hostname': hostname,
			'temp': sensor.get_temperature(),
			'pi_id': pi_id
			})

	return sensordata

while True:
	sensordata = getsensordata()
	res = requests.post(url, json = sensordata, headers = hdr)
	print("%s %s" % (res.status_code, res.text))
	time.sleep(interval)
