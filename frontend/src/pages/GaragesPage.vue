<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="12">
        <v-sheet min-height="80vh">
          <data-table
            title="Garages"
            :items="items"
            :headers="headers"
            :current-page="currentPage"
            :last-page="lastPage"
            @page-updated="(newPage) => (currentPage = newPage)"
          >
            <template v-slot:title="{ title }">
              <v-row>
                <v-col md="5">
                  <v-card-item class="ma-6 pa-2">
                    <v-text-field
                      label="Name, Address or Contact"
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
                    color="blue-lighten-1"
                    class="ma-6 pa-2"
                    @click="openModal"
                    >add
                  </v-btn>
                </v-col>
              </v-row>
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
                      :error-messages="errors.name"
                      :rules="rules.garage.nameRules"
                      label="Name"
                      required
                      v-model="data.name"
                      density="compact"
                      variant="underlined"
                      validate-on="lazy blur"
                      @input="clearError"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      label="Address"
                      :rules="rules.garage.addressRules"
                      v-model="data.address"
                      density="compact"
                      variant="underlined"
                      validate-on="lazy blur"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      :rules="rules.garage.contactRules"
                      label="Contact"
                      required
                      v-model="data.contact"
                      density="compact"
                      variant="underlined"
                      validate-on="lazy blur"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      :rules="rules.garage.phoneRules"
                      label="Phone"
                      required
                      v-model="data.phone"
                      density="compact"
                      variant="underlined"
                      @input="clearError"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      :rules="rules.garage.providerRules"
                      label="Provider"
                      required
                      v-model="data.grid_provider"
                      density="compact"
                      variant="underlined"
                      @input="clearError"
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
import { onMounted } from "vue";
import { useStore } from "vuex";
import DataTable from "@/components/DataTable";

import { useSubmitForm } from "@/use/form";
import { usePagination } from "@/use/pagination";
import { addGarage, listGarages } from "@/services/garages";
import { menuItems } from "@/menu/app-menu-items";
import { rules } from "@/configs/validation";

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
  itemSender: addGarage,
  afterHandler: (response) => {
    fetchData();
    if (!getters.currentGarage) {
      commit("setCurrentGarage", [response]);
    }
  },
});

const { currentPage, lastPage, fetchData, items, search } = usePagination({
  itemsLoader: listGarages,
  afterHandler: (items) => {
    commit("setGarages", items);
  },
});

onMounted(() => {
  const { commit } = useStore();
  commit("setPageMenuItems", menuItems);
});

const headers = [
  {
    title: "Name",
    key: "name",
    align: "right",
    sortable: false,
    width: "30%",
  },
  {
    title: "Address",
    key: "address",
    align: "center",
    sortable: false,
    width: "20%",
  },
  {
    title: "Contact",
    key: "contact",
    align: "center",
    sortable: false,
    width: "20%",
  },
  {
    title: "Phone",
    key: "phone",
    align: "center",
    sortable: true,
    width: "40%",
  },
];
</script>
