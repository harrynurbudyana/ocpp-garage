// Composables
import { createRouter, createWebHistory } from 'vue-router'
import AuthGuard from "./guards/auth-guard";
import PublicPageGuard from "./guards/public-page-guard";


const routes = [
  {
    path: "/login",
    name: "login",
    beforeEnter: PublicPageGuard,
    component: () =>
      import(/* webpackChunkName: "home" */ "@/pages/LoginPage.vue"),
    meta: {
      public: true,
    },
  },
  {
    path: '/',
    component: () => import('@/layouts/AppLayout.vue'),
    beforeEnter: AuthGuard,
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import(/* webpackChunkName: "home" */ '@/views/Home.vue'),
      },
      {
        path: 'stations',
        name: 'Stations',
        component: () => import(/* webpackChunkName: "home" */ '@/pages/StationsPage'),
      },
      {
        path: 'drivers',
        name: 'Drivers',
        component: () => import(/* webpackChunkName: "home" */ '@/pages/DriversPage'),
      },
      {
        path: 'transactions',
        name: 'Transactions',
        component: () => import(/* webpackChunkName: "home" */ '@/pages/TransactionsPage'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
