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
        name: 'Home',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "home" */ '@/views/Home.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
