<template>
  <v-container class="text-center" v-if="!loading">
    <div class="text-h5 mt-16">Choose your option.</div>
    <v-row justify="center" class="mt-16">
      <v-col cols="12" sm="6" md="4" v-for="amount in options" :key="amount">
        <v-btn
          block
          color="grey-lighten-3"
          rounded="sm"
          size="x-large"
          @click="() => onClick(amount)"
          >$ {{ amount / 100 }}
        </v-btn>
      </v-col>
    </v-row>
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
import { useRouter } from "vue-router";
import { onMounted, ref } from "vue";
import { requestCheckoutSession } from "@/services/payments";

const data = ref({});
const loading = ref(false);

const { currentRoute } = useRouter();
const options = [500, 1000, 1500, 2000]; // $ cents
const onClick = (amount) => {
  loading.value = true;
  data.value.amount = amount;
  requestCheckoutSession(data.value)
    .then((response) => (window.location.href = response.url))
    .finally(() => (loading.value = false));
};

onMounted(() => {
  data.value.charge_point_id = currentRoute.value.params.stationId;
  data.value.connector_id = currentRoute.value.params.connectorId;
});
</script>
