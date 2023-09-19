<template>
  <v-card
    max-width="100%"
    class="elevation-20 text-center"
    height="430"
    v-if="station"
  >
    <v-container>
      <v-card-actions>
        <v-row align="end">
          <v-col>
            <v-sheet>
              <v-btn variant="outlined" color="blue-darken-1">Edit</v-btn>
            </v-sheet>
          </v-col>
          <v-col>
            <v-sheet>
              <v-btn variant="outlined" color="grey-darken-1">Reset</v-btn>
            </v-sheet>
          </v-col>
          <v-col>
            <v-sheet>
              <v-btn
                variant="outlined"
                color="red"
                @click="removeStation(station.id)"
                >Delete</v-btn
              >
            </v-sheet>
          </v-col>
        </v-row>
      </v-card-actions>
    </v-container>
    <v-card-item>
      <v-card-title class="pt-4 mt-10 mb-3"> {{ station.id }} </v-card-title>

      <v-card-text class="mb-10">
        <v-chip :color="STATION_STATUS_COLOR[station.status.toLowerCase()]">
          <p class="text-medium-emphasis">
            {{ station.status }}
          </p>
        </v-chip>
        <div>
          <div class="text-h6 mb-1">
            {{ station.manufacturer }} / {{ station.model }}
          </div>
          <div class="text-overline mb-1">{{ station.location }}</div>
          <div class="text-caption">{{ station.description }}</div>
        </div>
      </v-card-text>
    </v-card-item>
  </v-card>

  <v-carousel
    v-if="station"
    height="400"
    class="mt-3 elevation-20"
    :show-arrows="showArrows()"
    hide-delimiter-background
  >
    <v-carousel-item
      v-for="(connectorId, i) in Object.keys(station.connectors)"
      :key="i"
    >
      <v-card max-width="100%" class="elevation-20 text-center" height="100%">
        <v-card-title primary-title>Connector</v-card-title>
        <v-card-subtitle class="mt-10 mb-10">
          <v-chip
            :color="
              STATION_STATUS_COLOR[
                station.connectors[connectorId].status.toLowerCase()
              ]
            "
          >
            <p class="text-medium-emphasis">
              {{ station.connectors[connectorId].status }}
            </p>
          </v-chip>
        </v-card-subtitle>
        <v-container>
          <v-row align="end" style="height: 170px">
            <v-col>
              <v-btn
                variant="outlined"
                color="grey-darken-1"
                @click="startRemoteTransaction(connectorId)"
                >Start</v-btn
              >
            </v-col>
            <v-col>
              <v-btn
                variant="outlined"
                color="grey-darken-1"
                @click="unlockConnector(connectorId)"
                >Unlock</v-btn
              >
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-carousel-item>
  </v-carousel>

  <empty-data v-if="!station"></empty-data>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { STATION_STATUS_COLOR } from "@/components/enums";

import { menuItems } from "@/menu/station-menu-items";
import { useStore } from "vuex";
import { getStation, deleteStation } from "@/services/stations";
import EmptyData from "@/components/EmptyData";

const station = ref();
const router = useRouter();
const { commit } = useStore();

const removeStation = (stationId) => {
  commit("setGlobalLoading");
  deleteStation(stationId)
    .then(() => {
      router.push({ name: "Stations" });
    })
    .finally(() => {
      commit("unsetGlobalLoading");
    });
};

const showArrows = () => {
  return Object.keys(station.value.connectors).length > 1;
};

const startRemoteTransaction = (connectorId) => {
  console.log("StartRemoteTransaction: ", connectorId);
};

const unlockConnector = (connectorId) => {
  console.log("UnlockConnector: ", connectorId);
};

onMounted(() => {
  commit("setPageMenuItems", menuItems);
  commit("setGlobalLoading");
  getStation(router.currentRoute.value.params.stationId)
    .then((response) => {
      station.value = response;
    })
    .finally(() => {
      commit("unsetGlobalLoading");
    });
});
</script>
