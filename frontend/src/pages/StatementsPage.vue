<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="12">
        <v-sheet min-height="80vh">
          <data-table
            title="Statements"
            :items="items"
            :headers="headers"
            :current-page="currentPage"
            :last-page="lastPage"
            @page-updated="(newPage) => (currentPage = newPage)"
          >
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
import { menuItems } from "@/menu/app-menu-items";
import { listStatements } from "@/services/statements";

const { currentPage, lastPage, items } = usePagination({
  itemsLoader: listStatements,
});

onMounted(() => {
  const { commit } = useStore();
  commit("setPageMenuItems", menuItems);
});

const headers = [
  {
    title: "Year",
    key: "year",
    align: "center",
    sortable: false,
    width: "20%",
  },
  {
    title: "Month",
    key: "month",
    align: "center",
    sortable: false,
    width: "20%",
  },
  {
    title: "Sum",
    key: "sum",
    align: "center",
    sortable: false,
    width: "20%",
  },
  {
    title: "Status",
    key: "status",
    align: "center",
    sortable: false,
    width: "20%",
  },
];
</script>
