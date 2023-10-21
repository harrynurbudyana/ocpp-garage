<template>
  <v-container>
    <v-col>
      <v-row justify="end">
        <v-btn color="blue-lighten-1 mr-2">Save</v-btn>
      </v-row>
      <v-row class="mt-10">
        <v-slider
          thumb-label="always"
          v-model="data.daily.garageRate"
          :max="1"
          :min="0.45"
          :step="0.01"
          hide-details
          class="align-center"
          color="grey"
          track-size="1"
        >
          <template v-slot:thumb-label="{ modelValue }">
            {{ countPercentage(modelValue, data.daily.providerRate) }}%
          </template>
          <template v-slot:prepend>
            <v-sheet class="text-caption mr-5">Daily rate:</v-sheet>
            <v-text-field
              disabled
              v-model="data.daily.providerRate"
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
              v-model="data.daily.garageRate"
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
      <v-row class="mt-10">
        <v-slider
          thumb-label="always"
          v-model="data.nightly.garageRate"
          :min="data.nightly.providerRate"
          :max="1"
          :step="0.01"
          hide-details
          class="align-center"
          color="grey"
          track-size="1"
        >
          <template v-slot:thumb-label="{ modelValue }">
            {{ countPercentage(modelValue, data.nightly.providerRate) }}%
          </template>
          <template v-slot:prepend>
            <v-sheet class="text-caption mr-2">Nightly rate:</v-sheet>
            <v-text-field
              disabled
              v-model="data.nightly.providerRate"
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
              v-model="data.nightly.garageRate"
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
import { reactive } from "vue";

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

const model = reactive({});
</script>
