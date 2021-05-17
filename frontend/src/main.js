import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import '../static/css/common.css'
import '../static/css/bootstrap.css'

createApp(App).use(router).mount('#app')
