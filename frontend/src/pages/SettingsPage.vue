<template>
  <v-container>
    <v-col>
      <v-row justify="end">
        <v-btn color="blue-lighten-1 mr-2">Save</v-btn>
      </v-row>
      <v-row class="mt-10" v-for="(key, i) in Object.keys(data)" :key="i">
        <v-slider
          thumb-label="always"
          v-model="data[key].garageRate"
          :max="1"
          :min="data[key].providerRate"
          :step="0.01"
          hide-details
          class="align-center"
          color="grey"
          track-size="1"
        >
          <template v-slot:thumb-label="{ modelValue }">
            {{ countPercentage(modelValue, data[key].providerRate) }}%
          </template>
          <template v-slot:prepend>
            <v-sheet class="text-caption mr-5">{{ key }} rate:</v-sheet>
            <v-text-field
              disabled
              v-model="data[key].providerRate"
              hide-details
              single-line
              type="float"
              variant="outlined"
              density="compact"
              style="width: 70px"
            ></v-text-field>
          </template>
          <template v-slot:append>
            <v-text-field
              v-model="data[key].garageRate"
              hide-details
              single-line
              type="float"
              variant="outlined"
              style="width: 70px"
              density="compact"
            ></v-text-field>
          </template>
        </v-slider>
      </v-row>
    </v-col>
  </v-container>
</template>

<script setup>
import { onMounted, reactive } from "vue";
import { menuItems } from "@/menu/app-menu-items";
import { useStore } from "vuex";

const { commit } = useStore();

const countPercentage = (newRate, initialRate) => {
  return Math.ceil(((newRate - initialRate) / initialRate) * 100);
};

const data = reactive({
  daily: {
    garageRate: 0.45,
    providerRate: 0.45,
  },
  nightly: {
    garageRate: 0.29,
    providerRate: 0.29,
  },
});

onMounted(() => {
  commit("setPageMenuItems", menuItems);
});
</script>
