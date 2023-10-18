<template>
  <v-card class="mx-auto text-center" width="100%" height="100%" v-if="garage">
    <v-card-title>
      {{ garage.name }}
    </v-card-title>
    <div class="mt-3">Address:</div>
    <v-card-subtitle> {{ garage.city }}, {{ garage.street }}</v-card-subtitle>
    <div class="mt-3">Contact:</div>
    <v-card-subtitle> {{ garage.contact }}</v-card-subtitle>
    <v-card-subtitle> {{ garage.email }}</v-card-subtitle>
    <v-card-subtitle> {{ garage.phone }}</v-card-subtitle>
    <div class="mt-3">Provider:</div>
    <v-card-subtitle> {{ garage.grid_provider }}</v-card-subtitle>
    <div class="mt-3">Postnummer:</div>
    <v-card-subtitle> {{ garage.postnummer }}</v-card-subtitle>
  </v-card>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useStore } from "vuex";
import { getGarage } from "@/services/garages";
import router from "@/router";

import { menuItems } from "@/menu/garage-menu-item";

const { commit } = useStore();
const garage = ref();

onMounted(() => {
  commit("setPageMenuItems", menuItems);
  commit("setGlobalLoading");
  getGarage(router.currentRoute.value.params.garageId)
    .then((response) => {
      garage.value = response;
    })
    .finally(() => {
      commit("unsetGlobalLoading");
    });
});
</script>
