<template>
  <div class="datamap view">
    <div class="menu">
      <ul @click="switchCity">
        <li v-for="city in cites" :key="city">
          <button class="btn">{{ city }}</button>
        </li>
      </ul>
    </div>

    <div id="map"></div>
  </div>
</template>

<script>
import { Loader } from "@googlemaps/js-api-loader";
export default {
  setup() {},
  data() {
    return {
      cites: ["Melbourne", "Sydney", "Brisbane"],
    };
  },
  beforeMount() {
    console.log(process.env.VUE_APP_GOOGLE_MAP_KEY);

    const loader = new Loader({
      apiKey: process.env.VUE_APP_GOOGLE_MAP_KEY,
      version: "weekly",
    });
    console.log(loader);
    loader.load().then(() => {
      // console.log(this.google)
      let map = new window.google.maps.Map(document.getElementById("map"), {
        center: { lat: -34.397, lng: 150.644 },
        zoom: 8,
      });
      this.map = window.map = map;
      // Define the LatLng coordinates for the outer path.
      map.data.loadGeoJson(
        "https://raw.githubusercontent.com/nholmber/google-maps-statistics/master/map_data_reduced.json"
      );
      map.data.addListener("click", function (event) {
        console.log(event);
      });
    });
  },
  methods: {
    switchCity(event) {
      let city = event.target.innerText;
      let coords = {};
      switch (city) {
        case "Melbourne":
          coords = { lat: -37.8069, lng: 144.9703 };
          break;
        case "Sydney":
          coords = { lat: -33.867, lng: 151.2045 };
          break;
        case "Brisbane":
          coords = { lat: -27.4673, lng: 153.0233 };
          break;
      }
      window.map.setZoom(10);
      window.map.setCenter(coords);
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