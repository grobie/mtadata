var interval;
var green = ['#0A9434', '#3BA95C', '#6CBE85', '#9DD4AD', '#CEE9D6'];
var red = ['#CC0200', '#D63433', '#E06766', '#EA9999', '#F4CCCC'];

$(document).ready(function() {
  L.mapbox.accessToken = 'pk.eyJ1IjoicGllcnJlcGllcnJlIiwiYSI6Ilk0NTlEcTAifQ.wb5BKEMZmXOC37hCDcC_lQ';

  var legendBox = $('<div id="legend" style="display: none;"></div>');
  var navBox = $('<nav class="legend clearfix"></nav>');
  for(var i = 0; i < red.length; i++){
    navBox.append('<span style="background:'+red[i]+';"></span>');
  }

  navBox.append('<span style="background:#ffffff;"></span>');

  for(var i = green.length-1; i >= 0; i--){
    navBox.append('<span style="background:'+green[i]+';"></span>');
  }

  for(var i = red.length; i > 0; i--){
    if(i % 2 != 0) navBox.append('<label>'+(i/red.length)*100+'%</label>');
  }

  navBox.append('<label>0%</label>');

  for(var i = 1; i <= green.length; i++){
    if(i % 2 != 0) navBox.append('<label>'+(i/green.length)*100+'%</label>');
  }

  $("#map").after(legendBox.append(navBox));
  var map = L.mapbox.map('map', 'examples.map-i86nkdio').setView([40.72, -73.902], 11);
  map.legendControl.addLegend(document.getElementById('legend').innerHTML);
  var time = "03/07/2015 00:00:00";

  function stationColor(traffic){
    if(traffic.entries == 0 && traffic.exits == 0){
      return '#ffffff';
    }

    if(traffic.entries > traffic.exits){
      var ratio = traffic.exits/traffic.entries;
      var color = green;
    } else {
      var ratio = traffic.entries/traffic.exits;
      var color = red;
    }

    return color[Math.floor(ratio*color.length)];
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

    function updateStations(time){
      $('#date').html(formatTime(time));

      map.featureLayer.setFilter(function(feature) {
        var properties = feature.properties;
        var traffic = properties.traffic[time.toString()];

        properties['marker-symbol'] = 'rail-metro';
        if (traffic) {
          properties['marker-color'] = stationColor(traffic);
          properties['description'] = traffic.entries + ' / ' + traffic.exits;
        } else {
          properties['marker-color'] = '#808080';
          properties['description'] = 'none';
        }
        return true;
      });
    }

    updateStations(timeMin.toString());
    map.featureLayer.setGeoJSON(stations);

    $( "#slider" ).slider({
      min: timeMin,
      max: timeMax,
      step: 3600,
      change: function(event, ui){
        timeCurrent = ui.value;
        updateStations(timeCurrent);
      },
      slide: function(event, ui){
        timeCurrent = ui.value;
        updateStations(timeCurrent);
      },
    });

    interval = setInterval(function(){
      if (timeCurrent == timeMax) {
        timeCurrent = timeMin;
      } else {
        timeCurrent += 3600;
      }
      $('#slider').slider('value', timeCurrent);
    }, 1000);
  });

});

function stop(){
  clearInterval(interval);
}

function componentToHex(c) {
    var hex = Math.round(c).toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function normalize(value, in_min, in_max, out_min, out_max) {
  return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

