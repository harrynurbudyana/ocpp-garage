<template>
  <v-card
    max-width="100%"
    class="elevation-20 text-center"
    height="430"
    v-if="station"
  >
    <v-container>
      <v-card-actions>
        <v-row>
          <v-col>
            <v-sheet align="left">
              <v-btn
                variant="outlined"
                color="blue-darken-1"
                @click="openModal('edit')"
                >Edit
              </v-btn>
            </v-sheet>
          </v-col>
          <v-col>
            <v-sheet align="right">
              <v-btn variant="outlined" color="red" @click="openConfirm()"
                >Delete
              </v-btn>
            </v-sheet>
          </v-col>
        </v-row>
      </v-card-actions>
    </v-container>
    <v-card-item>
      <v-card-title>
        <v-icon class="mdi mdi-ev-station"></v-icon>
        {{ station.location }}
      </v-card-title>

      <v-card-text class="mb-10">
        <v-chip :color="STATION_STATUS_COLOR[station.status]">
          <p class="text-medium-emphasis">
            {{ station.status }}
          </p>
        </v-chip>
        <div>
          <div class="text-h6 mb-1">
            {{ station.manufacturer }} / {{ station.model }}
          </div>
          <div class="text-overline mb-1">{{ station.id }}</div>
          <div class="text-caption">{{ station.description }}</div>
        </div>
      </v-card-text>
    </v-card-item>
    <v-container>
      <v-card-actions>
        <v-row align="end">
          <v-col></v-col>
          <v-col>
            <v-sheet>
              <v-btn variant="outlined" color="grey-darken-1">Reset</v-btn>
            </v-sheet>
          </v-col>
          <v-col></v-col>
        </v-row>
      </v-card-actions>
    </v-container>
  </v-card>

  <v-carousel
    v-if="station"
    height="400"
    class="mt-3 elevation-20"
    :show-arrows="showArrows()"
    hide-delimiters
  >
    <v-carousel-item
      v-for="(connectorId, i) in Object.keys(station.connectors)"
      :key="i"
    >
      <v-card max-width="100%" class="elevation-20 text-center" height="100%">
        <v-card-title primary-title>
          <span class="mdi mdi-connection"></span>
          Connector {{ connectorId }}
        </v-card-title>
        <v-card-subtitle class="mt-10 mb-10">
          <v-chip
            :color="
              STATION_STATUS_COLOR[station.connectors[connectorId].status]
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
                >Start
              </v-btn>
            </v-col>
            <v-col>
              <v-btn
                variant="outlined"
                color="grey-darken-1"
                @click="unlockConnector(connectorId)"
                >Unlock
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-carousel-item>
  </v-carousel>

  <empty-data v-if="!station"></empty-data>

  <v-form v-model="isValid">
    <v-container>
      <v-row justify="center">
        <v-dialog v-model="editDialog" persistent width="600">
          <v-card>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12">
                    <v-text-field
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
                @click="closeModal('edit')"
                :disabled="loading"
              >
                Close
              </v-btn>
              <v-btn
                color="blue-darken-1"
                variant="text"
                @click="editStation(station.id)"
                :loading="loading"
                :disabled="!isValid"
              >
                Edit
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
    </v-container>
  </v-form>

  <confirm-window :callback="() => removeStation(station.id)"></confirm-window>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { useConfirm } from "@/use/dialogs";

import { deleteStation, getStation, updateStation } from "@/services/stations";

import { STATION_STATUS_COLOR } from "@/components/enums";
import { menuItems } from "@/menu/station-menu-items";
import { rules } from "@/configs/validation";

import EmptyData from "@/components/EmptyData";
import ConfirmWindow from "@/components/dialogs/ConfirmWindow";

const loading = ref(false);
const isValid = ref(false);
const editDialog = ref(false);
const data = ref({});
const errors = ref({});
const showError = ref(false);
const station = ref();
const router = useRouter();
const { commit } = useStore();
const { openConfirm } = useConfirm();

const editStation = (stationId) => {
  loading.value = true;
  updateStation(stationId, data.value)
    .then((response) => {
      station.value = response;
      closeModal("edit");
    })
    .finally(() => {
      loading.value = false;
    });
};

const clearError = () => {
  showError.value = false;
  errors.value = {};
};

const openModal = (type) => {
  if (type === "edit") {
    editDialog.value = true;
  }
};

const closeModal = (type) => {
  if (type === "edit") {
    editDialog.value = false;
    data.value = {};
    clearError();
  }
};

const removeStation = (stationId) => {
  return deleteStation(stationId).then(() => {
    router.push({ name: "Stations" });
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

<style>
.private-button {
  width: 10%;
}
</style>
