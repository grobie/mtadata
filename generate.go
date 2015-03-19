package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
)

const (
	entrancesCsvFile = "data/station-entrances.csv"
	matchFirstRecord = 0
)

type point struct {
	lat, long float64
}

func newPoint(lat, long string) point {
	return point{parseCoordinate(lat), parseCoordinate(long)}
}

func (p point) String() string {
	return fmt.Sprintf("[%f,%f]", p.lat, p.long)
}

type station struct {
	name      string
	location  point
	lines     []string
	entrances []point
}

type feature struct {
	t string `json="type"`
	:q
}

func main() {
	csvFile, err := os.Open(entrancesCsvFile)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	defer csvFile.Close()

	reader := csv.NewReader(csvFile)
	reader.FieldsPerRecord = matchFirstRecord

	lines, err := reader.ReadAll()
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	stations := map[string]*station{}
	for line, f := range lines {
		if line == 0 {
			continue
		}

		name, sLat, sLong, eLat, eLong := f[2], f[3], f[4], f[28], f[29]
		s, ok := stations[name]
		if !ok {
			s = &station{
				name:      name,
				location:  newPoint(sLat, sLong),
				entrances: []point{},
			}
			stations[name] = s
		}

		s.entrances = append(s.entrances, newPoint(eLat, eLong))
	}

	for _, s := range stations {
		fmt.Printf(
			"station: %s (%s) has %d entrances: %s\n",
			s.name,
			s.location,
			len(s.entrances),
			s.entrances,
		)
	}
}

func parseCoordinate(c string) float64 {
	f, err := strconv.ParseFloat(c, 64)
	if err != nil {
		panic(err)
	}
	return f
}
