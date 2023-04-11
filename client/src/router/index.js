import { createRouter, createWebHashHistory } from 'vue-router'
const routes = [
  {
    path: '/',
    name: 'login',
    component: require("../views/login.vue").default
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
