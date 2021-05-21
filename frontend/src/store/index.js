import { createStore } from 'vuex'

export default createStore({
  state: {
    places: {
      vic: {
        n: 'vic',
        name: 'Victoria',
        coords: { lat: -36.13615274670763, lng: 144.75151428066573 },
        zoom: 7,
        filename: 'vic_plus.json'
      }, 
      nsw: {
        n: 'nsw',
        name: 'New South Wales',
        coords: { lat: -32.17623298515995, lng: 146.70449300679843 },
        zoom: 6,
        filename: 'nsw.json'
      }
    },
    scenarios: ['Bitcoin', 'Exercise', 'Traffic'],
    aurins: ['Population', 'Income', 'Obesity']
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})
