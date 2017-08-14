// request GeoJson data from USGS remote server
var url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson";

esriRequest(url, {
  responseType: "json"
}).then(function(response){
  // The requested data
  var geoJson = response.data;
});
