<template>
  <v-container class="text-center" v-if="!loading">
    <v-progress-circular
      class="mt-16"
      :rotate="360"
      :size="100"
      :width="15"
      :model-value="percentage"
      color="teal"
    >
      <template v-slot:default> {{ percentage }} %</template>
    </v-progress-circular>
    <div class="text-caption mt-16">
      {{ completed ? "Finished" : "Started" }}
      {{ dateAgo(completed ? data.updated_at : data.created_at) }}
    </div>
  </v-container>
  <v-container v-else class="text-center">
    <v-progress-circular
      class="mt-16"
      :size="100"
      :width="10"
      color="grey-lighten-3"
      indeterminate
    ></v-progress-circular>
  </v-container>
</template>
<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { trackProgress } from "@/services/transactions";
import { useRouter } from "vue-router";
import { TRANSACTIONS_STATUS } from "@/components/enums";
import { dateAgo } from "@/filters/date";

const { currentRoute } = useRouter();

const completed = ref(false);
const percentage = ref(0);
const loading = ref(true);
const data = ref({});

var trackId = null;
var interval = null;

const computePercentage = ({ meterStart, meterStop, limit }) => {
  let difference = meterStop - meterStart;
  return Math.ceil((100 * difference) / limit);
};

const watchProgress = () => {
  trackProgress(trackId).then((response) => {
    data.value = response;
    if (response.status !== TRANSACTIONS_STATUS.in_progress) {
      completed.value = true;
    }
    percentage.value = computePercentage({
      meterStart: response.meter_start,
      meterStop: response.meter_stop,
      limit: data.value.limit,
    });
  });
};

onMounted(() => {
  trackId = currentRoute.value.params.trackId;
  trackProgress(trackId)
    .then((response) => {
      data.value = response;
      percentage.value = computePercentage({
        meterStart: response.meter_start,
        meterStop: response.meter_stop,
        limit: data.value.limit,
      });
      if (response.status === TRANSACTIONS_STATUS.in_progress) {
        interval = setInterval(() => watchProgress(), 5000);
      } else {
        completed.value = true;
        clearInterval(interval);
      }
    })
    .finally(() => (loading.value = false));
});

onUnmounted(() => {
  clearInterval(interval);
});
</script>
