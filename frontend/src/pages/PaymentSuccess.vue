<template>
  <v-row align="center" justify="center" class="mt-16">
    <v-col>
      <v-card class="mx-auto" max-width="500" height="300" variant="elevated">
        <v-card-item>
          <div class="text-center">
            <v-progress-circular
              v-if="processing"
              :size="70"
              :width="7"
              color="green"
              indeterminate
            >
            </v-progress-circular>
            <v-icon
              v-else
              icon="mdi mdi-check-circle-outline"
              color="green"
              size="70"
            ></v-icon>
          </div>
          <v-card-title align="center" class="mt-10"
            >{{ processing ? "Processing..." : "Funds sent" }}
          </v-card-title>
        </v-card-item>
      </v-card>
    </v-col>
  </v-row>
</template>
<script setup>
import { ref } from "vue";

const processing = ref(false);
</script>
