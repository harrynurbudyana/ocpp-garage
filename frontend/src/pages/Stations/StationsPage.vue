<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="12">
        <v-sheet min-height="80vh">
          <data-table
            title="Stations"
            :items="items"
            :headers="headers"
            :current-page="currentPage"
            :last-page="lastPage"
            @page-updated="(newPage) => (currentPage = newPage)"
            @click-row="onClickRow"
          >
            <template v-slot:title="{ title }">
              <v-row>
                <v-col md="5">
                  <v-card-item class="ma-6 pa-2">
                    <v-text-field
                      label="Id, Status or Location"
                      density="compact"
                      variant="outlined"
                      append-inner-icon="mdi-magnify"
                      v-model="search"
                    >
                    </v-text-field>
                  </v-card-item>
                </v-col>
                <v-col class="d-flex justify-left mb-6">
                  <v-card-item>{{ title }}</v-card-item>
                </v-col>
                <v-col class="d-flex justify-end mb-6 mt-3">
                  <v-btn
                    v-if="permittedToAddStation(getters.currentUser)"
                    color="blue-lighten-1"
                    class="ma-6 pa-2"
                    @click="openModal"
                    >add
                  </v-btn>
                </v-col>
              </v-row>
            </template>
            <template v-slot:item.status="{ item }">
              <v-chip
                :color="STATION_STATUS_COLOR[item.columns.status.toLowerCase()]"
              >
                <p class="text-medium-emphasis">
                  {{ item.columns.status }}
                </p>
              </v-chip>
            </template>
          </data-table>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>

  <v-form v-model="isValid">
    <v-container>
      <v-row justify="center">
        <v-dialog v-model="dialog" persistent width="600">
          <v-card>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                      :error="showError && errors.id"
                      :error-messages="errors.id"
                      :rules="rules.station.idRules"
                      label="Id"
                      required
                      v-model="data.id"
                      density="compact"
                      variant="underlined"
                      validate-on="lazy blur"
                      @input="clearError"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      required
                      label="Location"
                      :rules="rules.station.locationRules"
                      v-model="data.location"
                      density="compact"
                      variant="underlined"
                      validate-on="lazy blur"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      :rules="rules.station.commentRules"
                      label="Description"
                      v-model="data.description"
                      density="compact"
                      variant="underlined"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions class="mb-7">
              <v-spacer></v-spacer>
              <v-btn
                color="blue-darken-1"
                variant="text"
                @click="closeModal"
                :disabled="loading"
              >
                Close
              </v-btn>
              <v-btn
                color="blue-darken-1"
                variant="text"
                @click="sendData"
                :loading="loading"
                :disabled="!isValid || loading"
              >
                Add
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
    </v-container>
  </v-form>
</template>

<script setup>
import { onMounted, onUnmounted } from "vue";
import { useStore } from "vuex";
import { dateAgo } from "@/filters/date";
import DataTable from "@/components/DataTable";
import { rules } from "@/configs/validation";
import router from "@/router";

import { STATION_STATUS_COLOR } from "@/components/enums";
import { usePagination } from "@/use/pagination";
import { addStation, listStations } from "@/services/stations";
import { menuItems } from "@/menu/app-menu-items";
import { useSubmitForm } from "@/use/form";

const { commit, getters } = useStore();

const {
  loading,
  isValid,
  dialog,
  data,
  errors,
  showError,
  clearError,
  openModal,
  closeModal,
  sendData,
} = useSubmitForm({
  itemSender: addStation,
  afterHandler: () => {
    fetchData();
  },
});

const { currentPage, lastPage, fetchData, items, search } = usePagination({
  itemsLoader: listStations,
});

var interval = null;

const permittedToAddStation = ({ is_admin, is_superuser }) => {
  return is_admin || is_superuser;
};

const onClickRow = ({ item }) => {
  router.push({
    name: "StationDetail",
    params: { stationId: item.columns.id },
  });
};

onMounted(() => {
  commit("setPageMenuItems", menuItems);
  interval = setInterval(() => fetchData({ periodic: 1 }), 5000);
});

onUnmounted(() => {
  clearInterval(interval);
});

const headers = [
  {
    title: "Id",
    key: "id",
    align: "right",
    sortable: false,
    width: "30%",
  },
  {
    title: "Status",
    key: "status",
    align: "center",
    sortable: false,
    width: "20%",
  },
  {
    title: "Location",
    key: "location",
    align: "center",
    sortable: false,
    width: "20%",
  },
  {
    title: "Last activity",
    key: "updated_at",
    align: "right",
    sortable: false,
    value: (v) => dateAgo(v.updated_at),
    width: "15%",
  },
];
</script>
