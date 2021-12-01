from datetime import datetime
import os
import sys
import requests
import socket
import time
import uuid
from w1thermsensor import W1ThermSensor
import sqlite3
import json

# Get settings from environment variables
url = os.getenv('URL')
sensors_api_key = os.getenv('SENSORS_API_KEY')
interval = os.getenv('INTERVAL')
hostname = socket.gethostname()

# Quit if settings in missing or ill formed
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

# Create database, if it does not already exists
con = sqlite3.connect('sensors.db')
cur = con.cursor()
cur.execute('''	CREATE TABLE IF NOT EXISTS measurements (
					timestamp text NOT NULL,
					thermostat_id text NOT NULL,
					hostname text NOT NULL,
					temp real NOT NULL,
					pi_id text NOT NULL,
					uuid text NOT NULL) ''')

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
		now = datetime.now().astimezone().isoformat()
		temp = sensor.get_temperature()
		print("Sensor %s has temperature %.2f" % (sensor.id, temp))
		sensordata.append({
			'timestamp': now,
			'thermostat_id': sensor.id,
			'hostname': hostname,
			'temp': temp,
			'pi_id': pi_id,
			'uuid': str(uuid.uuid4())
		})

	return sensordata

def write_measurements_to_database(measurements):
	for measurement in measurements:
		cur.execute('''INSERT INTO measurements VALUES (
							:timestamp,
							:thermostat_id,
							:hostname,
							:temp,
							:pi_id,
							:uuid)''',
							measurement)
	con.commit()

def read_measurements_from_database():
	measurements = []
	for measurement in cur.execute("SELECT * FROM measurements"):
		measurements.append({
			'timestamp': measurement[0],
			'thermostat_id': measurement[1],
			'hostname': measurement[2],
			'temp': measurement[3],
			'pi_id': measurement[4],
			'uuid': measurement[5]
		})
	return measurements

def remove_measurement_from_database(measurement):
	cur.execute("DELETE FROM measurements WHERE uuid = ?", [measurement['uuid']])
	con.commit()

while True:
	sensordata = getsensordata() #Read sensor data from the DS18B20 temperatures
	write_measurements_to_database(sensordata) # insert sensordata in DB
	uncommitted = read_measurements_from_database() # read from DB
	res = requests.post(url, json = uncommitted, headers = hdr) # post uncommitted
	# print("%s %s" % (res.status_code, res.text))
	ms = json.loads(res.text)
	print("Server http response code: %s\nAnd payload:" % (res.status_code))
	print(json.dumps(ms, sort_keys=True, indent=4))
	for measurement in ms: # Remove the measurements accepted by the server from the local database
		if measurement['status'] in ['accepted', 'already accepted']:
			remove_measurement_from_database(measurement)

	time.sleep(interval)
