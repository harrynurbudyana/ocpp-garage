<template>
  <v-layout class="rounded rounded-md">
    <v-app-bar class="px-3" flat density="compact">
      <v-row justify="end">
        <v-menu transition="slide-y-transition" v-if="getters.currentGarage">
          <template v-slot:activator="{ props }">
            <v-btn
              v-bind="props"
              :disabled="!getters.dropDownList.length"
              class="mr-6"
              width="200"
              >{{ getters.currentGarage.name }}
            </v-btn>
          </template>
          <v-list>
            <v-list-item v-for="(item, i) in getters.dropDownList" :key="i">
              <v-list-item-title @click="switchGarage(item)"
                >{{ item.name }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-row>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      :rail="rail"
      permanent
      @click="rail = false"
    >
      <v-list-item prepend-icon="mdi mdi-garage" title="NO1" nav>
        <template v-slot:append>
          <v-btn
            variant="text"
            icon="mdi-chevron-left"
            @click.stop="rail = !rail"
          ></v-btn>
        </template>
      </v-list-item>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item
          v-for="link in getters.pageMenuItems"
          :key="link.name"
          :to="link.getPath(getters)"
          :value="link.key"
          :title="link.name"
          :prepend-icon="link.icon"
          :active="isActive(link.name)"
          :disabled="!link.isActive(getters)"
        >
        </v-list-item>
      </v-list>
      <v-list density="compact" nav class="logout">
        <v-list-item
          key="logout"
          value="logout"
          title="Logout"
          prepend-icon="mdi mdi-logout"
          @click="store.dispatch('logout')"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main class="bg-grey-lighten-3">
      <v-progress-linear
        :indeterminate="getters.globalLoading"
        color="blue-lighten-3"
      ></v-progress-linear>
      <v-container>
        <v-row>
          <v-col cols="12" md="9">
            <v-sheet height="90vh" rounded="lg" class="elevation-4">
              <router-view></router-view>
            </v-sheet>
          </v-col>

          <v-col cols="12" md="3">
            <v-sheet rounded="lg" height="90vh" class="elevation-4">
              <v-container>
                <v-card
                  v-for="(action, i) in actions.slice(0, MAX_ACTIONS_LENGTH)"
                  width="100%"
                  density="compact"
                  variant="flat"
                  class="pt-1"
                >
                  <template v-slot:prepend>
                    <v-tooltip activator="parent" location="end"
                      >{{
                        {
                          pending: "pending",
                          completed: "success",
                          faulted: "faulted",
                        }[action.status]
                      }}
                    </v-tooltip>
                    <v-icon
                      size="x-small"
                      :color="ACTION_STATUS_COLOR[action.status]"
                    >
                      {{ ACTION_ICON[action.status] }}
                    </v-icon>
                  </template>
                  <template v-slot:title>
                    <span class="text-caption">{{ action.body }}</span>
                  </template>

                  <template v-slot:subtitle>
                    <span class="text-caption"
                      >station: {{ action.charge_point_id }}</span
                    >
                  </template>
                  <v-divider v-if="i < MAX_ACTIONS_LENGTH - 1"></v-divider>
                </v-card>
              </v-container>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-layout>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { onMounted, onUnmounted, ref } from "vue";
import store from "@/store";
import { listActions } from "@/services/actions";
import { ACTION_STATUS_COLOR } from "@/components/enums";

const MAX_ACTIONS_LENGTH = 11;

const { currentRoute, push } = useRouter();
const { getters, commit } = useStore();

var interval = null;
const drawer = ref(true);
const rail = ref(false);
const actions = ref([]);

const ACTION_ICON = {
  pending: "mdi mdi-clock-time-seven-outline",
  completed: "mdi mdi-check",
  faulted: "mdi mdi-cancel",
};

const isActive = (name) => {
  return currentRoute.value.name === name;
};

const switchGarage = (item) => {
  commit("setCurrentGarage", [item]);
  push({ name: currentRoute.value.name, params: { garageId: item.id } }).then(
    () => {
      location.reload();
    }
  );
};

onMounted(() => {
  let garageId = currentRoute.value.params?.garageId;
  if (garageId) {
    commit("setCurrentGarageById", garageId);
  }
  interval = setInterval(() => {
    listActions({ periodic: 1 }).then((response) => (actions.value = response));
  }, 2000);
});

onUnmounted(() => {
  clearInterval(interval);
});
</script>

<style scoped>
.logout {
  position: absolute;
  bottom: 30px;
}
</style>
