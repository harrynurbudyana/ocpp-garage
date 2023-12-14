// Composables
import { createRouter, createWebHistory } from "vue-router";
import AuthGuard from "./guards/auth-guard";
import PublicPageGuard from "./guards/public-page-guard";
import HomePageGuard from "@/router/guards/home-page-guard";

const routes = [
  {
    path: "/:stationId/connectors/:connectorId",
    name: "Payment",
    component: () =>
      import(/* webpackChunkName: "home" */ "@/pages/PaymentPage.vue"),
    meta: {
      public: true,
    },
  },
  {
    path: "/transactions/:trackId",
    name: "Progress",
    component: () =>
      import(/* webpackChunkName: "home" */ "@/pages/ProgressPage.vue"),
    meta: {
      public: true,
    },
  },
  {
    path: "/",
    name: "Home",
    beforeEnter: HomePageGuard,
    meta: {
      public: true,
    },
  },
  {
    path: "/404",
    name: "404",
    component: () =>
      import(/* webpackChunkName: "home" */ "@/pages/NotFoundPage.vue"),
    meta: {
      public: true,
    },
  },
  {
    path: "/signup/:userId",
    name: "SignUp",
    component: () =>
      import(/* webpackChunkName: "home" */ "@/pages/Users/SighUpPage.vue"),
    meta: {
      public: true,
    },
  },
  {
    path: "/login",
    name: "Login",
    beforeEnter: PublicPageGuard,
    component: () =>
      import(/* webpackChunkName: "home" */ "@/pages/Users/LoginPage.vue"),
    meta: {
      public: true,
    },
  },
  {
    path: "/",
    component: () => import("@/layouts/AppLayout.vue"),
    beforeEnter: AuthGuard,
    children: [
      {
        path: "garages",
        name: "Garages",
        component: () =>
          import(
            /* webpackChunkName: "home" */ "@/pages/Garages/GaragesPage.vue"
          ),
      },
      {
        path: "garages/:garageId",
        name: "GarageDetail",
        component: () =>
          import(
            /* webpackChunkName: "home" */ "@/pages/Garages/GarageDetailPage.vue"
          ),
      },
      {
        path: ":garageId/stations",
        name: "Stations",
        component: () =>
          import(
            /* webpackChunkName: "home" */ "@/pages/Stations/StationsPage.vue"
          ),
      },
      {
        path: ":garageId/stations/:stationId",
        name: "StationDetail",
        component: () =>
          import(
            /* webpackChunkName: "home" */ "@/pages/Stations/StationDetailPage.vue"
          ),
        meta: {
          hasBackButton: true,
        },
      },
      {
        path: ":garageId/users",
        name: "Users",
        component: () =>
          import(/* webpackChunkName: "home" */ "@/pages/Users/UsersPage"),
      },
      {
        path: ":garageId/users/:driverId",
        name: "UserDetail",
        component: () =>
          import(
            /* webpackChunkName: "home" */ "@/pages/Users/UserDetailPage.vue"
          ),
        meta: {
          hasBackButton: true,
        },
      },
      {
        path: ":garageId/transactions",
        name: "Transactions",
        component: () =>
          import(/* webpackChunkName: "home" */ "@/pages/TransactionsPage.vue"),
      },
      {
        path: ":garageId/settings",
        name: "Settings",
        component: () =>
          import(/* webpackChunkName: "home" */ "@/pages/SettingsPage.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
