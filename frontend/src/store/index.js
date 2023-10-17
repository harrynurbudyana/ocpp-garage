import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

import auth from "@/store/modules/auth";
import navigation from "@/store/modules/navigation";
import garages from "@/store/modules/garages";

const getDefaultState = () => {
  return {
    loading: false,
  };
};

const state = getDefaultState();

export default createStore({
  state: state,
  mutations: {
    setGlobalLoading(state) {
      state.loading = true;
    },
    unsetGlobalLoading(state) {
      state.loading = false;
    },
  },
  actions: {},
  getters: {
    globalLoading(state) {
      return state.loading;
    },
  },
  modules: {
    auth,
    navigation,
    garages,
  },
  plugins: [
    createPersistedState({
      key: "usr.src.csms.data",
      paths: ["auth", "garages"],
    }),
  ],
});
