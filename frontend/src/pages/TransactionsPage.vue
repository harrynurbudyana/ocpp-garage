<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="12">
        <v-sheet min-height="90vh">
          <data-table
            title="Transactions"
            :items="items"
            :headers="headers"
            :current-page="currentPage"
            :last-page="lastPage"
            @page-updated="(newPage) => (currentPage = newPage)"
          >
            <template v-slot:title="{ title }">
              <v-row>
                <v-col>
                  <v-card-item class="ma-6 pa-2">
                    <v-text-field
                      label="Driver or Station"
                      density="compact"
                      variant="outlined"
                      append-inner-icon="mdi-magnify"
                      v-model="search"
                    >
                    </v-text-field>
                  </v-card-item>
                </v-col>
                <v-col class="d-flex justify-center mb-6">
                  <v-card-item>{{ title }}</v-card-item>
                </v-col>
                <v-col class="d-flex justify-end mb-6 mt-3"></v-col>
              </v-row>
            </template>
            <template v-slot:item.action="{ item }">
              <v-hover v-slot="{ isHovering, props }" open-delay="100">
                <v-btn
                  v-if="isStopStransactionAllowed(item)"
                  icon
                  size="small"
                  density="compact"
                  :elevation="isHovering ? 12 : 2"
                  :class="{ 'on-hover': isHovering }"
                  v-bind="props"
                  @click="() => stopTransaction(item)"
                >
                  <v-tooltip activator="parent" location="end"
                    >Stop transaction
                  </v-tooltip>
                  <v-icon color="deep-orange-lighten-3">mdi mdi-cancel</v-icon>
                </v-btn>
              </v-hover>
            </template>
          </data-table>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { onMounted } from "vue";
import { useStore } from "vuex";
import DataTable from "@/components/DataTable";

import { usePagination } from "@/use/pagination";
import {
  listTransactions,
  remoteStopTransaction,
} from "@/services/transactions";
import { menuItems } from "@/menu/app-menu-items";
import { dateAgo } from "@/filters/date";

const { currentPage, lastPage, items, search } = usePagination({
  itemsLoader: listTransactions,
});

const isStopStransactionAllowed = (item) => {
  return !item.selectable.meter_stop;
};

const stopTransaction = (item) => {
  remoteStopTransaction(item.key);
};

onMounted(() => {
  const { commit } = useStore();
  commit("setPageMenuItems", menuItems);
});

const headers = [
  {
    title: "Driver",
    key: "driver",
    align: "center",
    sortable: false,
    width: "20%",
  },
  {
    title: "Station",
    key: "charge_point",
    align: "center",
    sortable: false,
    width: "20%",
  },
  {
    title: "Connector",
    key: "connector",
    align: "center",
    sortable: false,
    width: "5%",
  },
  {
    title: "Started at",
    key: "created_at",
    align: "center",
    width: "20%",
    sortable: false,
    value: (v) => dateAgo(v.created_at),
  },
  {
    title: "Stopped at",
    align: "center",
    width: "20%",
    sortable: false,
    key: "updated_at",
    value: (v) => dateAgo(v.updated_at),
  },
  {
    title: "Consumed (kWh)",
    align: "center",
    width: "10%",
    sortable: false,
    value: (v) => v.meter_stop - v.meter_start,
    key: "consumed",
  },
  {
    title: "Action",
    align: "left",
    width: "15%",
    sortable: false,
    key: "action",
  },
];
</script>
