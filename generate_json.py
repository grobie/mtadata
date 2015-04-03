import csv
import json
import sys

class Station:
	def __init__(self, name, line, lat, long):
		self.name = name
		self.line = line
		self.lat = lat
		self.long = long
		self.entries = 0
		self.exits = 0

	def color(self):
		if self.entries > self.exits:
			return '#32cd32'
		else:
			return '#cd5c5c'

	def ratio(self):
		return float(self.entries) / float(self.exits)

def normalize(name):
	s = name
	if s.endswith('Av'):
		s = s + 'e'
	return s.upper()

stations = {}

with open('data/station-entrances.csv', newline='') as station_entrances:
	reader = csv.DictReader(station_entrances)
	for row in reader:
		name = row['Station_Name']
		line = row['Route_1']
		lat  = row['Station_Latitude']
		long = row['Station_Longitude']

		stations[normalize(name)] = Station(name, line, lat, long)

with open('data/turnstile.csv', newline='') as turnstile_csv:
	reader = csv.DictReader(turnstile_csv)
	for row in reader:
		name = normalize(row['STATION'])
		if stations.get(name) == None:
			continue

		for key in row:
			if key.startswith('EXITS'):
				exits = int(row[key])
				break

		stations[name].entries += int(row['ENTRIES'])
		stations[name].exits += exits

features = []
for key in stations:
	station = stations[key]

	# skip if no match. Sorry stations without exits.
	if station.exits == 0:
		continue

	features.append({
		'type': 'Feature',
		'geometry': {
			'type': 'Point',
			'coordinates': [station.long, station.lat]
		},
		'properties': {
			'title': station.name,
			'description': 'Line: ' + station.line + '<br />' +
				'Entries / Exits: ' + str(station.entries) + ' / ' + str(station.exits) + '<br />' +
				'Ratio: ' + str(round(station.ratio(), 2)),
			'line': station.line,
			'entries': station.entries,
			'exits': station.exits,
			'marker-symbol': 'rail-metro',
			'marker-color': station.color(),
		},
	})
geojson = {'type': 'FeatureCollection', 'features': features }

print('Dumping .geojson for', len(features), 'stations', file=sys.stderr)
print(json.dumps(geojson, sort_keys=True))
