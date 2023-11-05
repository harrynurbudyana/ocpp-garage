<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="12">
        <v-sheet min-height="80vh">
          <data-table
            title="Government rebates"
            :items="items"
            :headers="headers"
            :current-page="currentPage"
            :last-page="lastPage"
            @page-updated="(newPage) => (currentPage = newPage)"
          >
            <template v-slot:title="{ title }">
              <v-row>
                <v-col md="5">
                  <v-card-item class="ma-6 pa-2"></v-card-item>
                </v-col>
                <v-col class="d-flex justify-left mb-6">
                  <v-card-item>{{ title }}</v-card-item>
                </v-col>
                <v-col class="d-flex justify-end mb-6 mt-3">
                  <v-btn
                    :loading="loading"
                    color="blue-lighten-1"
                    class="ma-6 pa-2"
                    @click="openModal"
                    >add
                  </v-btn>
                </v-col>
              </v-row>
            </template>
            <template v-slot:item.action="{ item }">
              <v-hover v-slot="{ isHovering, props }" open-delay="100">
                <v-btn
                  icon
                  size="small"
                  density="compact"
                  :elevation="isHovering ? 12 : 2"
                  :class="{ 'on-hover': isHovering }"
                  :loading="trashLoading"
                  :disabled="trashLoading"
                  v-bind="props"
                  @click="removeRebate(item)"
                >
                  <v-icon color="deep-orange-lighten-3"
                    >mdi-trash-can-outline
                  </v-icon>
                </v-btn>
              </v-hover>
            </template>
          </data-table>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
  <v-form v-model="isValid">
    <v-container>
      <v-row justify="center">
        <v-dialog v-model="dialog" persistent width="400">
          <v-card height="400">
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12">
                    <v-sheet width="100%">
                      <VueDatePicker v-model="data.period" month-picker />
                    </v-sheet>
                  </v-col>
                  <v-col cols="12" class="mt-16">
                    <v-text-field
                      :disabled="!data.period"
                      :rules="rules.rebate.valueRules"
                      required
                      label="Rebate"
                      v-model="data.value"
                      density="compact"
                      variant="underlined"
                      validate-on="lazy"
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
                @click="() => handleRequest(data)"
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
import moment from "moment";
import { onMounted, ref } from "vue";
import { useStore } from "vuex";
import DataTable from "@/components/DataTable";

import { usePagination } from "@/use/pagination";
import {
  addGovernmentRebate,
  deleteGovernmentRebate,
  listGovernmentRebates,
} from "@/services/government_rebates";
import { menuItems } from "@/menu/app-menu-items";
import { useSubmitForm } from "@/use/form";
import { rules } from "@/configs/validation";

const {
  loading,
  isValid,
  dialog,
  data,
  clearError,
  openModal,
  closeModal,
  sendData,
} = useSubmitForm({
  itemSender: addGovernmentRebate,
  afterHandler: () => fetchData(),
});

const { currentPage, lastPage, fetchData, items } = usePagination({
  itemsLoader: listGovernmentRebates,
});

const trashLoading = ref(false);

const handleRequest = (data) => {
  let month = data.period.month + 1;
  let year = data.period.year;
  data.month = month;
  data.year = year;
  sendData();
};

const removeRebate = (item) => {
  trashLoading.value = true;
  deleteGovernmentRebate(item.key).then(() => {
    trashLoading.value = false;
    fetchData();
  });
};

onMounted(() => {
  const { commit } = useStore();
  commit("setPageMenuItems", menuItems);
});

const headers = [
  {
    title: "Period",
    key: "period",
    align: "right",
    value: (item) => {
      let check = moment(String(item.period)).local();
      return `${check.format("YYYY")} - ${check.format("MMMM")}`;
    },
    sortable: false,
    width: "30%",
  },
  {
    title: "Rebate",
    key: "value",
    align: "center",
    sortable: false,
    width: "30%",
  },
  {
    title: "Actions",
    align: "center",
    width: "10%",
    sortable: false,
    key: "action",
  },
];
</script>
