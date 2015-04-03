MTA_DATA_URL      ?= http://web.mta.info/developers/data
MTA_COLORS_URL    ?= $(MTA_DATA_URL)/colors.csv
MTA_ENTRANCES_URL ?= $(MTA_DATA_URL)/nyct/subway/StationEntrances.csv
MTA_TURNSTILE_URL ?= $(MTA_DATA_URL)/nyct/turnstile/turnstile_150314.txt

run: web/public/data/mta-stations.geojson
	cd web && node server.js

clean:
	rm -fr data mta-entrances.json

web/public/data/mta-stations.geojson: data/turnstile.csv data/station-entrances.csv generate_json.py
	python3 generate_json.py | jq . > $@

data:
	mkdir -p $@

data/turnstile.csv:
	curl $(MTA_TURNSTILE_URL) > $@

data/colors.csv: | data
	curl $(MTA_COLORS_URL) | grep -vE '^(MTA|,|")' > $@

data/station-entrances.csv: | data
	curl $(MTA_ENTRANCES_URL) > $@

