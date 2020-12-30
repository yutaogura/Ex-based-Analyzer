import Vue from 'vue'
import VueSidebarMenu from 'vue-sidebar-menu'
//import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
library.add(fas)
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.use(VueSidebarMenu)

// import VueRouter from 'vue-router'
// import Installation from '../components/Installation.vue'
// Vue.use(VueRouter)

// const router = new VueRouter({
//     routes: [
//       {
//         path: '/installation',
//         name: 'Installation',
//         component: Installation
//       },
//     //   {
//     //     path: '/props',
//     //     name: 'Props',
//     //     component: Props
//     //   },
//     //   {
//     //     path: '/events',
//     //     name: 'Events',
//     //     component: Events
//     //   },
//     //   {
//     //     path: '/styling',
//     //     name: 'Styling',
//     //     component: Styling
//     //   }
//     ]
//   })

//   new Vue({ // eslint-disable-line no-new
//     el: '#app',
//     router,
//     render: h => h(App)
//   })