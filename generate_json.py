import csv
import json
import re
import sys
from datetime import datetime

class Station:
	def __init__(self, name, line, lat, long):
		self.name = name
		self.line = line
		self.lat = lat
		self.long = long
		self.traffic = {}
		self.trafficPrevious = {}


def ord(n):
	return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))



def normalize(name):
	s = name.upper()

	if s.endswith('AV'):
		s = s + 'E'

	s = re.sub('([0-9]+) (ST|AVE)', lambda m: "{0} {1}".format(
		ord(int(m.group(1))).upper(), m.group(2)
	), s)

	return s

assert '121ST ST' == normalize('121 ST')

stations = {}

with open('data/station-entrances.csv', newline='') as station_entrances:
	reader = csv.DictReader(station_entrances)
	for row in reader:
		name = row['Station_Name']
		line = row['Route_1']
		lat  = row['Station_Latitude']
		long = row['Station_Longitude']
		key  = normalize(name)

		stations[key] = Station(name, line, lat, long)

with open('data/turnstile.csv', newline='') as turnstile_csv:
	reader = csv.DictReader(turnstile_csv)
	for row in reader:
		device = row['SCP']
		timeString = row['DATE'] +' '+ row['TIME']
		time = int(datetime.strptime(timeString, '%m/%d/%Y %H:%M:%S').timestamp())
		name = normalize(row['STATION'])
		if stations.get(name) == None:
			continue

		for key in row:
			if key.startswith('EXITS'):
				exitsAbsolute = int(row[key])
				break

		entriesAbsolute = int(row['ENTRIES'])
		

		if stations[name].trafficPrevious.get('device') == device:
			entriesRelative = entriesAbsolute - stations[name].trafficPrevious['entries']
			exitsRelative = exitsAbsolute - stations[name].trafficPrevious['exits']
		else:
			entriesRelative = 0
			exitsRelative = 0
			
		stations[name].trafficPrevious = {'entries': entriesAbsolute, 'exits': exitsAbsolute, 'device': device}
		if stations[name].traffic.get(time):
			stations[name].traffic[time]['entries'] += entriesRelative
			stations[name].traffic[time]['exits'] += exitsRelative
		else:
			stations[name].traffic[time] = {'entries': entriesRelative, 'exits': exitsRelative}
		

features = []
for key in stations:
	station = stations[key]

	# skip if no match. Sorry stations without exits.
	if station.traffic == {}:
		continue

	features.append({
		'type': 'Feature',
		'geometry': {
			'type': 'Point',
			'coordinates': [station.long, station.lat]
		},
		'properties': {
			'title': station.name,
			'line': station.line,
			'traffic': station.traffic,
		},
	})
features = sorted(features, key=lambda k: k['properties']['title'])
geojson = {'type': 'FeatureCollection', 'features': features }

print('Dumping .geojson for' , len(features), 'of', len(stations), 'stations', file=sys.stderr)
print(json.dumps(geojson, sort_keys=True, indent=2, separators=(',', ': ')))
