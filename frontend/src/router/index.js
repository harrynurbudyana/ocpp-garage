// Composables
import { createRouter, createWebHistory } from "vue-router";
import AuthGuard from "./guards/auth-guard";
import PublicPageGuard from "./guards/public-page-guard";
import HomePageGuard from "@/router/guards/home-page-guard";

const routes = [
  {
    path: "/",
    name: "Home",
    beforeEnter: HomePageGuard,
    meta: {
      public: true,
    },
  },
  {
    path: "/payments/success",
    name: "successPayment",
    component: () =>
      import(/* webpackChunkName: "home" */ "@/pages/PaymentSuccess.vue"),
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
    path: "/payments/:token",
    name: "payment",
    component: () =>
      import(/* webpackChunkName: "home" */ "@/pages/PaymentPage.vue"),
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
        name: "garages",
        component: () =>
          import(/* webpackChunkName: "home" */ "@/pages/GaragesPage"),
      },
      {
        path: "garages/:garageId",
        name: "SingleGarage",
        component: () =>
          import(/* webpackChunkName: "home" */ "@/pages/SingleGaragePage"),
      },
      {
        path: ":garageId/stations",
        name: "stations",
        component: () =>
          import(/* webpackChunkName: "home" */ "@/pages/StationsPage.vue"),
      },
      {
        path: ":garageId/stations/:stationId",
        name: "SingleStation",
        component: () =>
          import(
            /* webpackChunkName: "home" */ "@/pages/SingleStationPage.vue"
          ),
        meta: {
          hasBackButton: true,
        },
      },
      {
        path: ":garageId/drivers",
        name: "drivers",
        component: () =>
          import(/* webpackChunkName: "home" */ "@/pages/DriversPage"),
      },
      {
        path: ":garageId/drivers/:driverId",
        name: "SingleDriver",
        component: () =>
          import(/* webpackChunkName: "home" */ "@/pages/SingleDriverPage.vue"),
        meta: {
          hasBackButton: true,
        },
      },
      {
        path: ":garageId/operators",
        name: "operators",
        component: () =>
          import(/* webpackChunkName: "home" */ "@/pages/OperatorsPage"),
      },
      {
        path: ":garageId/operators/:operatorId",
        name: "SingleOperator",
        component: () =>
          import(
            /* webpackChunkName: "home" */ "@/pages/SingleOperatorPage.vue"
          ),
        meta: {
          hasBackButton: true,
        },
      },
      {
        path: ":garageId/transactions",
        name: "transactions",
        component: () =>
          import(/* webpackChunkName: "home" */ "@/pages/TransactionsPage"),
      },
      {
        path: ":garageId/government-rebates",
        name: "government-rebates",
        component: () =>
          import(
            /* webpackChunkName: "home" */ "@/pages/GovernmentRebatesPage"
          ),
      },
      {
        path: ":garageId/settings",
        name: "settings",
        component: () =>
          import(/* webpackChunkName: "home" */ "@/pages/SettingsPage"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
