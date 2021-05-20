<template>
  <div class="datamap view">
    <div class="menu">
      <ul @click="switchCity">
        <li v-for="city in cites" :key="city">
          <button class="btn">{{ city }}</button>
        </li>
      </ul>
      <div id="main" style="height:200px; width:200px"></div>
    </div>

    <div id="map"></div>
    <div class="footer">
      <select name="" id="">
        <option value="">Melbourne</option>
      </select>
    </div>
  </div>
</template>

<script>
import { Loader } from "@googlemaps/js-api-loader";
import * as echarts from 'echarts';
export default {
  setup() {},
  data() {
    return {
      cites: ["Melbourne", "Sydney", "Brisbane", "Finland"],
    };
  },
  beforeMount() {
    // let google = window.google;
    console.log(process.env.VUE_APP_GOOGLE_MAP_KEY);

    const loader = new Loader({
      apiKey: process.env.VUE_APP_GOOGLE_MAP_KEY,
      version: "weekly",
    });
    console.log(loader);
    loader.load().then(() => {
      let map = new window.google.maps.Map(document.getElementById("map"), {
        center: { lat: -37.8069, lng: 144.9703 },
        zoom: 8,
      });
      this.map = window.map = map;
      // Define the LatLng coordinates for the outer path.
      // map.data.loadGeoJson(
      //   "https://raw.githubusercontent.com/nholmber/google-maps-statistics/master/map_data_reduced.json"
      //   // "http://localhost:9000/qldgeo.json"
      // );

      var chartDom = document.getElementById('main');
      var myChart = echarts.init(chartDom);
      var option;

      option = {
          xAxis: {
              type: 'category',
              data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
          },
          yAxis: {
              type: 'value'
          },
          series: [{
              data: [120, 200, 150, 80, 70, 110, 130],
              type: 'bar',
              showBackground: true,
              backgroundStyle: {
                  color: 'rgba(180, 180, 180, 0.2)'
              }
          }]
      };

      option && myChart.setOption(option);


      var infowindow = new window.google.maps.InfoWindow();
      map.data.addListener("click", function (event) {
        console.log(event.feature.i);
        createInfoWindow(map, event, infowindow);
      });

      function createInfoWindow(map, event) {
        // Get properties from Data Layer to populate info window
        let name = event.feature.getProperty("vic_lga__3");
        let bit_count = event.feature.getProperty("tweets_count");
        let income_2013 = event.feature.getProperty("income_2013");
        let income_2014 = event.feature.getProperty("income_2014");

        // var zip = event.feature.getProperty("zip");
        // var income = event.feature.getProperty("income");
        // var incomeRelative = event.feature.getProperty("income_relative");
        // var population = event.feature.getProperty("pop2018");
        // var populationDensity = event.feature.getProperty("pop_density");

        // Create content for info window
        // var contentString =
        //   '<div id="content"><div id="siteNotice"></div>' +
        //   '<h2 id="firstHeading" class="firstHeading">' +
        //   name +
        //   "</h2>" +
        //   "<h3>Zip code: " +
        //   zip +
        //   "</h3>" +
        //   '<div id="bodyContent" style="font-size: 12pt;" >' +
        //   "</br>Population (2018): " +
        //   population +
        //   "</br>Median income (2015): " +
        //   income.toFixed(2) +
        //   " €" +
        //   "</br>Median income relative to national average (2015): " +
        //   incomeRelative.toFixed(2) +
        //   " €" +
        //   "</br>Population density (persons / km<sup>2</sup>): " +
        //   populationDensity.toFixed(2) +
        //   "</p>" +
        //   "</div>" +
        //   "</div>";
        let contentString = `<div id="content">
            <div id="siteNotice"></div>
            <h5 id="firstHeading" class="firstHeading">${name}</h5>
            <ul>
              <li>Tweet Counts: ${bit_count}</li>
              <li>Income of 2013: ${income_2013}</li>
              <li>Income of 2013: ${income_2014}</li>
            </ul>
           </div>`;

        // Center info window on selected zip code area
        // Find center of zip code area by converting
        // the corresponding Polygon object to a
        // LatLngBounds object which has the getCenter function
        var bounds = new window.google.maps.LatLngBounds();
        var geometry = event.feature.getGeometry();

        geometry.forEachLatLng(function (point) {
          bounds.extend({
            lat: point.lat(),
            lng: point.lng(),
          });
        });
        var center = bounds.getCenter();

        // Create invisible marker for info window
        var marker = new window.google.maps.Marker({
          position: center,
          map: map,
          visible: false,
        });
        // Create info window
        infowindow.setContent(contentString);
        infowindow.open(map, marker);
      }
    });
  },
  methods: {
    switchCity(event) {
      let city = event.target.innerText;
      let url;
      let coords = {};
      let map = window.map;
      window.map.data.forEach(function (feature) {
        window.map.data.remove(feature);
      });
      switch (city) {
        case "Melbourne":
          coords = { lat: -37.8069, lng: 144.9703 };
          url = "http://localhost:9000/vic_plus.json";
          break;
        case "Sydney":
          coords = { lat: -33.867, lng: 151.2045 };
          url = "http://localhost:9000/nsw.json";
          break;
        case "Brisbane":
          coords = { lat: -27.4673, lng: 153.0233 };
          url = "http://localhost:9000/qld.json";
          break;
        case "Finland":
          coords = { lat: 60.192059, lng: 24.945831 };
      }
      window.map.setZoom(10);
      window.map.setCenter(coords);
      window.map.data.loadGeoJson(url);

      console.log('start')
      map.data.forEach(function (feature) {
        console.log(feature.getProperty("tweets_count"))
        feature.setStyle()
      });
      console.log('end')
    },
  },
};
</script>

<style scoped>
.about {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
#map {
  width: 100%;
  height: 100%;
}
.menu {
  position: absolute;
  left: 0;
  top: 72px;
  z-index: 100;
  background: #fff;
}
</style>