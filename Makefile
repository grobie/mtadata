MTA_DATA_URL      ?= http://web.mta.info/developers/data
MTA_COLORS_URL    ?= $(MTA_DATA_URL)/colors.csv
MTA_ENTRANCES_URL ?= $(MTA_DATA_URL)/nyct/subway/StationEntrances.csv
MTA_TURNSTILE_URL ?= $(MTA_DATA_URL)/nyct/turnstile/turnstile_150314.txt

.PHONY: server
server: generate
	cd web && node server.js

.PHONY: generate
generate: web/public/data/mta-stations.geojson

.PHONY: clean
clean:
	rm -fr data web/public/data/mta-stations.geojson

.PHONY: publish
publish: web/public/data/mta-stations.geojson web/public/index.html
	git checkout gh-pages
	git checkout master -- $^
	git mv -f web/public/data/* data
	git mv -f web/public/index.html .
	git commit -m Publish
	git push origin gh-pages
	git checkout master

web/public/data/mta-stations.geojson: data/station-entrances.csv data/turnstile.csv generate_json.py
	python3 generate_json.py | jq . > $@

data:
	mkdir -p $@

data/turnstile.csv: | data
	curl $(MTA_TURNSTILE_URL) > $@

data/colors.csv: | data
	curl $(MTA_COLORS_URL) | grep -vE '^(MTA|,|")' > $@

data/station-entrances.csv: | data
	curl $(MTA_ENTRANCES_URL) > $@
