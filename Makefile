MTA_DATA_URL      ?= http://web.mta.info/developers/data
MTA_COLORS_URL    ?= $(MTA_DATA_URL)/colors.csv
MTA_ENTRANCES_URL ?= $(MTA_DATA_URL)/nyct/subway/StationEntrances.csv

all: mta-entrances.json

clean:
	rm -fr data mta-entrances.json

mta-entrances.json: data/colors.csv data/station-entrances.csv
	go run generate.go

data:
	mkdir -p $@

data/colors.csv: | data
	curl $(MTA_COLORS_URL) | grep -vE '^(MTA|,|")' > $@

data/station-entrances.csv: | data
	curl $(MTA_ENTRANCES_URL) > $@
