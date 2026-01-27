import { createRouter, createWebHistory } from 'vue-router'
import FirstPage from '../pages/FirstPage.vue'
import SecondPage from '../pages/SecondPage.vue'
import Realty from '../pages/Realty.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/first-page',
      name: 'first',
      component: FirstPage,
    },
    {
      path: '/second-page',
      name: 'second',
      component: SecondPage,
    },
    {
      path: '/realty',
      name: 'realty',
      component: Realty,
    }
  ],
})

export default router
