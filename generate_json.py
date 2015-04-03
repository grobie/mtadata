import csv
import json
import re
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
features = sorted(features, key=lambda k: k['properties']['title'])
geojson = {'type': 'FeatureCollection', 'features': features }

print('Dumping .geojson for', len(features), 'of', len(stations), 'stations', file=sys.stderr)
print(json.dumps(geojson, sort_keys=True, indent=2, separators=(',', ': ')))
