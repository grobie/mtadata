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
    var lastTrafficKeys = Object.keys(stations[stations.length-1].properties.traffic);
    var timeMax = parseInt(lastTrafficKeys[lastTrafficKeys.length-1]);
    var timeMin = parseInt(Object.keys(stations[0].properties.traffic)[0]);

    function setStations(time){
      for(var i = 0; i < stations.length; i++){
            var properties = stations[i].properties;

            if(properties.traffic[time]){
                properties['marker-color'] = stationColor(properties.traffic[time]);
            }
            properties['marker-symbol'] = 'rail-metro';
          }
          map.featureLayer.setGeoJSON(stations); 
    }

    setStations(timeMin.toString());

    $( "#slider" ).slider({
      min: timeMin,
      max: timeMax,
      step: 3600,
      slide: function(event, ui){
        var currentTime = ui.value.toString();
        setStations(currentTime);
      }
    });
  });

});


