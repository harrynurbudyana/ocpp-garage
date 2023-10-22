<template>
  <v-container>
    <v-col>
      <v-row justify="end">
        <v-btn
          :disabled="disabled"
          :loading="loading"
          color="blue-lighten-1 mr-2"
          @click="onSaveChanges"
          >Save
        </v-btn>
      </v-row>
      <v-row class="mt-10" v-for="(period, i) in Object.keys(rates)" :key="i">
        <v-slider
          thumb-label="always"
          v-model="rates[period].garage_rate"
          :max="rates[period].provider_rate * 1.3"
          :min="rates[period].provider_rate"
          :step="0.01"
          hide-details
          class="align-center"
          color="grey"
          track-size="1"
          @update:modelValue="onUpdateSlider"
        >
          <template v-slot:thumb-label="{ modelValue }">
            {{ countPercentage(modelValue, rates[period].provider_rate) }}%
          </template>
          <template v-slot:prepend>
            <div class="text-caption mr-5">
              <v-sheet width="100px"
                >{{ period.charAt(0).toUpperCase() + period.slice(1) }} rate:
              </v-sheet>
            </div>
            <v-text-field
              disabled
              v-model="rates[period].provider_rate"
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
              disabled
              v-model="rates[period].garage_rate"
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
import { onMounted, reactive, ref } from "vue";
import { menuItems } from "@/menu/app-menu-items";
import { useStore } from "vuex";
import { getGarageRates, saveSettings } from "@/services/garages";

const { commit } = useStore();

const rates = reactive({
  daily: { garage_rate: 0.0, provider_rate: 0.0 },
  nightly: { garage_rate: 0.0, provider_rate: 0.0 },
});

const disabled = ref(true);
const loading = ref(false);

const countPercentage = (newRate, initialRate) => {
  return Math.ceil(((newRate - initialRate) / initialRate) * 100);
};

const onSaveChanges = () => {
  loading.value = true;
  let data = { rates };
  saveSettings(data).finally(() => {
    setTimeout(() => {
      loading.value = false;
      disabled.value = true;
    }, 1000);
  });
};

const onUpdateSlider = () => {
  disabled.value = false;
};

onMounted(() => {
  commit("setPageMenuItems", menuItems);
  getGarageRates().then((response) => {
    Object.assign(rates, response);
  });
});
</script>
