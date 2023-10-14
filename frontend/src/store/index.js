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
  actions: {
    initAction({ getters, commit }, payload) {
      // We don't want to make unnecessary request to the backend in case it's
      // a public page, it may effect Page Load Time
      if (!payload.isPublicPage && getters.isAuthorized) {
        return this.dispatch("getUser")
          .then(() => {
            if (getters.currentUser.is_superuser) {
              this.dispatch("getGarages");
            } else {
              commit("setCurrentGarage", getters.currentUser.id);
            }
          })
          .catch(() => {
            console.log("Wasn't able to receive user data");
          });
      } else {
        return Promise.resolve();
      }
    },
  },
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
      paths: ["auth"],
    }),
  ],
});
