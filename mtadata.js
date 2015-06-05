$(document).ready(function() {
  L.mapbox.accessToken = 'pk.eyJ1IjoicGllcnJlcGllcnJlIiwiYSI6Ilk0NTlEcTAifQ.wb5BKEMZmXOC37hCDcC_lQ';

  var map = L.mapbox.map('map', 'examples.map-i86nkdio').setView([40.72, -73.902], 11);
  var time = "03/07/2015 00:00:00";

  function stationColor(traffic){
          if(traffic.entries > traffic.exits){
              return '#32cd32';
          }else{
              return '#cd5c5c';
          }
  }

  jQuery.getJSON('data/mta-stations.geojson', function(data){
          var stations = data.features;

          for(var i = 0; i < stations.length; i++){
              var properties = stations[i].properties;

              if(properties.traffic[time]){
                  properties['marker-color'] = stationColor(properties.traffic[time]);
              }
              properties['marker-symbol'] = 'rail-metro';
          }

          map.featureLayer.setGeoJSON(stations);
  });
});
