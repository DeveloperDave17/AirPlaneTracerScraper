import time
from datetime import datetime, date
from unittest import TestCase, skipIf
import mysql.connector

from opensky_api import FlightData, FlightTrack, OpenSkyApi, StateVector, Waypoint

OPENSKY_USERNAME = ""
OPENSKY_PASSWORD = ""

db = mysql.connector.connect(
    host="",
    port= 000,
    user="",
    passwd="",
    database=""
)

mycursor = db.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS StateVector ( state_vector_id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, icao24 VARCHAR(24) NOT NULL, callsign VARCHAR(20), origin_country VARCHAR(56), time_position INT, last_contact INT, longitude FLOAT NOT NULL, latitude FLOAT NOT NULL, baro_altitude FLOAT NOT NULL, on_ground BOOLEAN, velocity FLOAT, true_track FLOAT, vertical_rate FLOAT, geo_altitude FLOAT, squawk VARCHAR(4), spi BOOLEAN, position_source INT, category INT, received_time TIME, received_date DATE);")

api = OpenSkyApi(OPENSKY_USERNAME, OPENSKY_PASSWORD)

while True:
	states = api.get_states()
	currentDate = date.today()
	now = datetime.now()

	timeOfPull = now.strftime("%H:%M:%S")

	if states is not None:
		for state in states.states:
			if state.longitude != None and state.latitude != None and state.baro_altitude != None:	
				mycursor.execute("INSERT INTO StateVector (icao24, callsign, origin_country, time_position, last_contact, longitude, \
		      						latitude, geo_altitude, on_ground, velocity, true_track, vertical_rate, baro_altitude, squawk, spi, \
		      						position_source, category, received_time, received_date) \
		     						VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
									(state.icao24, state.callsign, state.origin_country, state.time_position, state.last_contact,
	   								 state.longitude, state.latitude, state.geo_altitude, state.on_ground, state.velocity, 
									 state.true_track, state.vertical_rate, state.baro_altitude, state.squawk, state.spi, state.position_source,
									 state.category, timeOfPull, currentDate))
				db.commit()

	after = datetime.now()
	afterPull = after.strftime("%H:%M:%S")
	delta = datetime.strptime(afterPull,"%H:%M:%S") - datetime.strptime(timeOfPull,"%H:%M:%S")
	timedif = delta.total_seconds()
	if timedif < 120:
		time.sleep(120 - timedif)




