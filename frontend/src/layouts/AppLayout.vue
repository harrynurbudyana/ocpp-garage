<template>
  <v-layout class="rounded rounded-md">
    <v-app-bar title="Application bar"></v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      :rail="rail"
      permanent
      @click="rail = false"
    >
      <v-list-item
        prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg"
        title="John Leider"
        nav
      >
        <template v-slot:append>
          <v-btn
            variant="text"
            icon="mdi-chevron-left"
            @click.stop="rail = !rail"
          ></v-btn>
        </template>
      </v-list-item>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item
          v-for="link in links"
          :key="link.name"
          :to="link.path"
          :value="link.key"
          :title="link.name"
          :prepend-icon="link.icon"
          :active="isActive(link.name)"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main class="bg-grey-lighten-3">
      <v-progress-linear
        :indeterminate="store.getters.globalLoading"
        color="blue-lighten-3"
      ></v-progress-linear>
      <v-container>
        <v-row>
          <v-col cols="12" sm="12">
            <v-sheet min-height="90vh">
              <router-view></router-view>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-layout>
</template>

<script setup>
import {ref} from "vue";
import store from "@/store";
import router from "@/router";

const drawer = ref(true);
const rail = ref(false);

const isActive = (name) => {
  return router.currentRoute.value.name === name;
}

const links = [
  {
    name: "Dashboard",
    key: "dashboard",
    path: "/",
    icon: "mdi-home-city",
  },
  {
    name: "Stations",
    path: "/stations",
    key: "stations",
    icon: "mdi mdi-ev-station",
  },
  {
    name: "Drivers",
    path: "/drivers",
    key: "drivers",
    icon: "mdi mdi-card-account-details-outline",
  },
  {
    name: "Transactions",
    path: "/transactions",
    key: "transactions",
    icon: "mdi mdi-battery-charging-outline",
  },
];
</script>
