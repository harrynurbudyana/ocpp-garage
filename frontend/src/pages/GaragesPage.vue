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
            @click-row="onClickRow"
          >
            <template v-slot:title="{ title }">
              <v-row>
                <v-col md="5">
                  <v-card-item class="ma-6 pa-2">
                    <v-text-field
                      label="Name, City, Contact or Post nummer"
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
                    :loading="postNummersLoading"
                    color="blue-lighten-1"
                    class="ma-6 pa-2"
                    @click="showModal"
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
                      :error="!!errors.name"
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
                      label="City"
                      required
                      :rules="rules.garage.cityRules"
                      v-model="data.city"
                      density="compact"
                      variant="underlined"
                      validate-on="lazy blur"
                      @input="clearError"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      label="Street"
                      required
                      :rules="rules.garage.addressRules"
                      v-model="data.street"
                      density="compact"
                      variant="underlined"
                      validate-on="lazy blur"
                      @input="clearError"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      required
                      :rules="rules.garage.contactRules"
                      label="Contact"
                      v-model="data.contact"
                      density="compact"
                      variant="underlined"
                      validate-on="lazy blur"
                      @input="clearError"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      required
                      :rules="rules.garage.phoneRules"
                      label="Phone"
                      v-model="data.phone"
                      density="compact"
                      variant="underlined"
                      @input="clearError"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      label="E-mail"
                      required
                      :rules="rules.garage.emailRules"
                      v-model="data.email"
                      density="compact"
                      variant="underlined"
                      validate-on="lazy blur"
                      @input="clearError"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-autocomplete
                      :items="grid_providers"
                      v-model="data.grid_provider_id"
                      required
                      label="Postnummer"
                      density="compact"
                      variant="underlined"
                      item-title="postnummer"
                      item-value="id"
                      @update:modelValue="onUpdatePostnummer"
                    ></v-autocomplete>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      required
                      label="Provider"
                      v-model="grid_provider_name"
                      density="compact"
                      variant="underlined"
                      disabled
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
import { onMounted, ref } from "vue";
import { useStore } from "vuex";
import DataTable from "@/components/DataTable";

import { useSubmitForm } from "@/use/form";
import { usePagination } from "@/use/pagination";
import { addGarage, listGarages } from "@/services/garages";
import { menuItems } from "@/menu/app-menu-items";
import { rules } from "@/configs/validation";
import router from "@/router";
import { listGridProviders } from "@/services/grid-providers";

const { commit, getters } = useStore();
const grid_providers = ref([]);
const grid_provider_name = ref();
const postNummersLoading = ref(false);

const {
  loading,
  isValid,
  dialog,
  data,
  errors,
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

const onUpdatePostnummer = (value) => {
  grid_provider_name.value =
    grid_providers.value.filter((item) => item.id === value)[0]?.name || null;
};

const showModal = () => {
  postNummersLoading.value = true;
  listGridProviders()
    .then((response) => (grid_providers.value = response))
    .finally(() => {
      openModal();
      postNummersLoading.value = false;
    });
};

const { currentPage, lastPage, fetchData, items, search } = usePagination({
  itemsLoader: listGarages,
  afterHandler: (items) => {
    commit("setGarages", items);
  },
});

const onClickRow = ({ item }) => {
  router.push({
    name: "SingleGarage",
    params: { garageId: item.key },
  });
};

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
    width: "20%",
  },
  {
    title: "City",
    key: "city",
    align: "right",
    sortable: false,
    width: "20%",
  },
  {
    title: "Street",
    key: "street",
    align: "right",
    sortable: false,
    width: "30%",
  },
  {
    title: "Contact",
    key: "contact",
    align: "right",
    sortable: false,
    width: "30%",
  },
];
</script>
