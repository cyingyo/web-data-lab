import Vue from 'vue'
import Router from 'vue-router'

import Movies from '@/views/Movies'
import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/hello',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/',
      name: 'Movies',
      component: Movies
    }
  ]
})
