<template>
  <div class="datamap view">
    <div id="map"></div>
    <div class="footer">
      <div class="container">
        <div class="filters">
          <div class="input-group">
            <label class="input-group-text" for="sel_pla">Place</label>
            <select
              class="form-select"
              id="sel_pla"
              @change="switchPlace($event)"
            >
              <option v-for="place in places" :key="place" :value="place.n">
                {{ place.name }}
              </option>
            </select>
          </div>

          <div class="input-group">
            <label class="input-group-text" for="sel_sce">Twitter Data</label>
            <select
              class="form-select"
              id="sel_sce"
              @change="switchScenario($event)"
            >
              <option v-for="scenario in scenarios" :key="scenario">
                {{ scenario }}
              </option>
            </select>
          </div>

          <div class="input-group">
            <label class="input-group-text" for="sel_aur">Aurin Data</label>
            <select
              class="form-select"
              id="sel_aur"
              @change="switchAurin($event)"
            >
              <option v-for="aurin in aurins" :key="aurin">{{ aurin }}</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Loader } from "@googlemaps/js-api-loader";
import * as echarts from "echarts";
export default {
  setup() {},
  data() {
    return {
      currentPlace: null,
      currentScenario: null,
      currentAurin: null,
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

      this.switchPlace("vic");

      this.infowindow = new window.google.maps.InfoWindow();

      map.data.addListener("click", (event) => {
        console.log(event.feature.i);
        this.createInfoWindow(map, event);
      });
    });
  },
  mounted() {
    this.currentScenario = document.getElementById("sel_sce").value;
    this.currentAurin = document.getElementById("sel_aur").value;
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
    switchPlace(event) {
      this.clearMap();
      let n = event.target?.value || event;
      let { coords, zoom, filename } = this.places[n];
      let map = this.map;
      let url = process.env.VUE_APP_BACKEND_BASE_URL + filename;
      this.currentPlace = this.places[n];

      console.log(coords);
      map.setZoom(zoom);
      map.setCenter(coords);
      map.data.loadGeoJson(url);
      // map.data.forEach(function (feature) {
      //   // map.data.remove(feature);

      // });
    },
    switchScenario(e) {
      this.currentScenario = e.target.value;
      this.infowindow.close();
      console.log("switch scenario", e);
    },
    switchAurin(e) {
      this.currentAurin = e.target.value;
      this.infowindow.close();
      console.log("switch aurin", e);
    },
    createInfoWindow(map, event) {
      console.log(this.currentScenario);
      console.log(this.currentAurin);
      let name = event.feature.getProperty(this.currentPlace.placeField);

      let bitcoin_tweets_count = event.feature.getProperty(
        "bitcoin_tweets_count"
      );
      let traffic_tweets_count = event.feature.getProperty(
        "traffic_tweets_count"
      );
      let exercise_tweets_count = event.feature.getProperty(
        "exercise_tweets_count"
      );

      let income = event.feature.getProperty("income_2014");
      let obesity = event.feature.getProperty("obesity_rate");
      let population = event.feature.getProperty("population");

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

      let obesityPieChart = `<div id="obesityPieChart" style="height:240px;width:300px;"></div>`;
      let contentString = `<div id="content">
            <div id="siteNotice">${this.currentPlace.name}</div>
            <h5 id="firstHeading" class="firstHeading">${name}</h5>
            <div id="bodyContent">
              <ul>
                <li>Bitcoin Tweet Counts: ${bitcoin_tweets_count}</li>
                <li>Traffic Tweet Counts: ${traffic_tweets_count}</li>
                <li>Exercise Tweet Counts: ${exercise_tweets_count}</li>
                <li>Income of 2014: ${income}</li>
                <li>Obesity: ${obesity}</li>
                <li>Population: ${population}</li>
              </ul>
              ${obesity && this.currentAurin === 'Obesity' ? obesityPieChart : ''}
            </div>
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

      // import * as echarts from 'echarts';

      if (obesity && this.currentAurin === "Obesity") {
        setTimeout(() => {
          var chartDom = document.getElementById("obesityPieChart");
          var myChart = echarts.init(chartDom);
          var option;

          option = {
            tooltip: {
              trigger: "item",
            },
            legend: {
              top: "0%",
              left: "center",
            },
            series: [
              {
                name: "Obesity Rate",
                type: "pie",
                radius: ["40%", "70%"],
                avoidLabelOverlap: false,
                itemStyle: {
                  borderRadius: 10,
                  borderColor: "#fff",
                  borderWidth: 2,
                },
                label: {
                  show: true,
                  // position: 'center',
                  formatter: "{d}%",
                },
                emphasis: {
                  // label: {
                  //   show: true,
                  //   fontSize: "40",
                  //   fontWeight: "bold",
                  // },
                },
                labelLine: {
                  show: true,
                },
                data: [
                  { value: obesity, name: "Obesity" },
                  { value: population - obesity, name: "Other" },
                ],
              },
            ],
          };

          option && myChart.setOption(option);
        }, 0);
      }
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

.footer {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 72px;
  background: #fff;
}

.filters {
  display: flex;
  justify-content: space-between;
}

.filters > .input-group {
  width: 30%;
}
</style>