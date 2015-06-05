$(document).ready(function() {
  L.mapbox.accessToken = 'pk.eyJ1IjoicGllcnJlcGllcnJlIiwiYSI6Ilk0NTlEcTAifQ.wb5BKEMZmXOC37hCDcC_lQ';

  var map = L.mapbox.map('map', 'examples.map-i86nkdio').setView([40.72, -73.902], 11);
  var time = "03/07/2015 00:00:00";

  function stationColor(traffic){
    if(traffic.entries > traffic.exits){
      return '#32cd32';
    } else {
      return '#cd5c5c';
    }
  }

  function formatZero(number) {
    if (number < 10) {
      return '0' + number.toString();
    } else {
      return number.toString();
    }
  }

  function formatTime(time) {
    var a = new Date(time*1000);
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = formatZero(a.getDate());
    var hour = formatZero(a.getHours());
    var min = formatZero(a.getMinutes());
    var sec = formatZero(a.getSeconds());

    return month + ', ' + date + ' ' + year + ' ' + hour + ':' + min + ':' + sec;
  }

  jQuery.getJSON('data/mta-stations.geojson', function(data){
    var stations = data.features;
    var lastTrafficKeys = Object.keys(stations[stations.length-1].properties.traffic);
    var timeMin = parseInt(Object.keys(stations[0].properties.traffic)[0]);
    var timeMax = parseInt(lastTrafficKeys[lastTrafficKeys.length-1]);
    var timeCurrent = timeMin;

    function setStations(time){
      $('#date').html(formatTime(time));

      for(var i = 0; i < stations.length; i++){
        var properties = stations[i].properties;
        var traffic = properties.traffic[time.toString()];

        if (traffic) {
          properties['marker-color'] = stationColor(traffic);
        } else {
          properties['marker-color'] = '#808080';
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
      change: function(event, ui){
        timeCurrent = ui.value;
        setStations(timeCurrent);
      },
      slide: function(event, ui){
        timeCurrent = ui.value;
        setStations(timeCurrent);
      },
    });

    setInterval(function(){
      if (timeCurrent == timeMax) {
        timeCurrent = timeMin;
      } else {
        timeCurrent += 3600;
      }
      $('#slider').slider('value', timeCurrent);
    }, 500);
  });

});


