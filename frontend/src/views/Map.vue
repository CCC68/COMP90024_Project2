<template>
  <div class="datamap view">
    <div class="menu">
      <ul @click="switchCity">
        <li v-for="city in cites" :key="city">
          <button class="btn">{{ city }}</button>
        </li>
      </ul>
      <div id="main" style="height: 200px; width: 200px"></div>
    </div>

    <div id="map"></div>
    <div class="footer">

      <div class="input-group">
        <label class="input-group-text" for="sel_pla">Place</label>
        <select class="form-select" id="sel_pla" @change="switchPlace($event.target.value)">
          <option v-for="place in places" :key="place" :value="place.n">{{ place.name }}</option>
        </select>
      </div>

      <div class="input-group">
        <label class="input-group-text" for="sel_sce">Twitter Data</label>
        <select class="form-select" id="sel_sce">
          <option v-for="scenario in scenarios" :key="scenario">{{ scenario }}</option>
        </select>
      </div>

      <div class="input-group">
        <label class="input-group-text" for="sel_aur">Aurin Data</label>
        <select class="form-select" id="sel_aur">
          <option v-for="aurin in aurins" :key="aurin">{{ aurin }}</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
import { Loader } from "@googlemaps/js-api-loader";
// import * as echarts from "echarts";
export default {
  setup() {},
  data() {
    return {
      cites: ["Melbourne", "Sydney", "Brisbane", "Finland"],
    };
  },
  beforeMount() {

    this.initData();

    const loader = new Loader({
      apiKey: process.env.VUE_APP_GOOGLE_MAP_KEY,
      version: "weekly",
    });

    loader.load().then(() => {
      let map = new window.google.maps.Map(document.getElementById("map"), {
        // Map Options like 'center' & 'zoom'
      });
      
      this.map = window.map = map;

      this.switchPlace('vic');

      this.infowindow = new window.google.maps.InfoWindow();

      map.data.addListener("click", (event) => {
        console.log(event.feature.i);
        this.createInfoWindow(map, event);
      });

    });
  },
  methods: {
    initData() {
      this.places = this.$store.state.places;
      this.scenarios = this.$store.state.scenarios;
      this.aurins = this.$store.state.aurins;
      this.google = window.google;
    },
    clearMap() {
      let map = this.map;
      this.infowindow?.close();
      map.data.forEach(function (feature) {
        map.data.remove(feature);
      });
    },
    switchPlace(n) {

      this.clearMap();

      let { coords, zoom, filename } = this.places[n];
      let map = this.map;
      let url = process.env.VUE_APP_BACKEND_BASE_URL + filename;

      console.log(coords);
      map.setZoom(zoom);
      map.setCenter(coords);
      map.data.loadGeoJson(url);

    },
    createInfoWindow(map, event) {

        let name = event.feature.getProperty("vic_lga__3");
        let bit_count = event.feature.getProperty("tweets_count");
        let income_2013 = event.feature.getProperty("income_2013");
        let income_2014 = event.feature.getProperty("income_2014");

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
        this.infowindow.setContent(contentString);
        this.infowindow.open(map, marker);
      }
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
.footer {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
}
</style>