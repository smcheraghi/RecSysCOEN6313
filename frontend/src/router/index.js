import Vue from 'vue'
import Router from 'vue-router'

import Ping from '@/pages/Ping'
import Home from '@/pages/Home'
import About from '@/pages/About'

// const routerOptions = [
//   { path: '/', component: 'Home' },
//   { path: '/ping', component: 'Ping' },
//   { path: '/about', component: 'About' },
//   { path: '*', component: '404' }
// ]

// const routes = routerOptions.map(route => {
//   return {
//     ...route,
//     component: () =>
//       import(`@/pages/${route.component}.vue`)
//   }
// })

// Vue.use(Router)

// export default new Router({
//   routes,
//   mode: 'history'
// })
Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/about',
      name: 'About',
      component: About
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping
    }
  ]
})
