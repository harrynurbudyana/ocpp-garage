<template>
  <div class="text-center">
    <v-progress-circular
      indeterminate
      color="primary"
      size="500px"
    ></v-progress-circular>
  </div>
</template>

<script setup>
import { onBeforeMount } from "vue";
import { useRouter } from "vue-router";
import { createPaymentSession, verifyPayment } from "@/services/payments";

const { currentRoute } = useRouter();

onBeforeMount(() => {
  verifyPayment(currentRoute.value.params.token).then((data) => {
    createPaymentSession(data).then((response) => {
      window.location.href = response.url;
    });
  });
});
</script>
