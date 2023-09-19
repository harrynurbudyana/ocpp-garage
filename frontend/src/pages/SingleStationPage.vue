<template>Single station</template>

<script setup>
import { onMounted } from "vue";

import { menuItems } from "@/menu/station-menu-items";
import { useStore } from "vuex";

onMounted(() => {
  const { commit } = useStore();
  commit("setPageMenuItems", menuItems);
});
</script>
