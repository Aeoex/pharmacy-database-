import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import About from '@/views/About.vue'
import Signup from '@/views/Signup.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup
    },
  ]
})

export default router
