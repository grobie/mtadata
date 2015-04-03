import csv
import json

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


stations = {}

with open('data/station-entrances.csv', newline='') as station_entrances:
	reader = csv.DictReader(station_entrances)
	for row in reader:
		name = row['Station_Name']
		line = row['Route_1']
		lat = row['Station_Latitude']
		long = row['Station_Longitude']
		stations[name.upper()] = Station(name, line, lat, long)

with open('data/turnstile.csv', newline='') as turnstile_csv:
	reader = csv.DictReader(turnstile_csv)
	for row in reader:
		name = row['STATION'].upper()
		if stations.get(name) == None:
			continue

		for key in row:
			if key.startswith('EXITS'):
				exits = int(row[key])
				break

		stations[name].entries += int(row['ENTRIES'])
		stations[name].exits += exits

features = []
for upper in stations:
	station = stations[upper]

	# skip if no match. Sorry stations without exits.
	if station.exits == 0:
		continue

	# TODO(grobie): generate JSON
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

print(json.dumps({'type': 'FeatureCollection', 'features': features }))
