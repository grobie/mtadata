import csv

class Station:
	def __init__(self, name, line, lat, long):
		self.name = name
		self.line = line
		self.lat = lat
		self.long = long

stations = map{}

with open('data/turnstile.csv', newline='') as turnstile_csv:
	reader = csv.DictReader(turnstile_csv)
	count = 0
	for row in reader:
		count=count+1
		if count == 1:
			continue
		print ((row['UNIT']))
		
		if count > 5:
			break


with open('data/turnstile.csv', newline='') as turnstile_csv:
	reader = csv.DictReader(turnstile_csv)
	count = 0
	for row in reader:
		count=count+1
		if count == 1:
			continue
		print ((row['UNIT']))
		
		if count > 5:
			break