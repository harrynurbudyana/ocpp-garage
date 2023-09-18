import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

import auth from "@/store/modules/auth";

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
      state.loading = true;
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
  },
  plugins: [
    createPersistedState({
      key: "usr.src.csms.data",
      paths: ["auth"]
    })
  ]
});
