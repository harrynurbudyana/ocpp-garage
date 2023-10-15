import router from "@/router";
import { request } from "@/api";

const getDefaultState = () => {
  return {
    isAuthorized: false,
    user: {
      is_superuser: false,
    },
  };
};

const state = getDefaultState();

function _processSuccessfulLogout(commit) {
  commit("unsetAuthorized");
  commit("unsetUser");
  commit("unsetCurrentGarage");
  commit("usetGarages");
  router.push("/login");
}

function _processSuccessfulLogin(commit, userData) {
  let operator = userData.operator;
  let garages = userData.garages;
  commit("setAuthorized");
  commit("setUser", operator);
  commit("setCurrentGarage", garages);

  if (operator.is_superuser) {
    router.push("/garages");
  } else {
    router.push(`${garages[0].id}/stations`);
  }
}

export default {
  name: "auth",
  state,
  actions: {
    initAction({ getters }, payload) {
      // We don't want to make unnecessary request to the backend in case it's
      // a public page, it may effect Page Load Time
      if (!payload.isPublicPage && getters.isAuthorized) {
        this.dispatch("getUser").catch(() => {
          console.log("Wasn't able to receive user data");
        });
      } else {
        return Promise.resolve();
      }
    },
    getUser({ commit }) {
      return request.get("/me").then((responseBody) => {
        commit("setUser", responseBody.operator);
        commit("setGarages", responseBody.garages);
        commit("setCurrentGarage", responseBody.garages);
      });
    },

    silentLogout({ commit }) {
      _processSuccessfulLogout(commit);
    },

    logout() {
      request.post("/logout");
    },

    login({ commit }, credentials) {
      return request.post("/login", credentials).then((responseBody) => {
        if (responseBody) {
          _processSuccessfulLogin(commit, responseBody);
        } else {
          console.error("Login data is missing");
        }
      });
    },
  },
  getters: {
    currentUser(state) {
      return state.user;
    },

    isAuthorized(state) {
      return state.isAuthorized;
    },
    currentGarageId(state) {
      return state.currentGarageId;
    },
  },

  mutations: {
    setAuthorized(state) {
      state.isAuthorized = true;
    },

    unsetAuthorized(state) {
      state.isAuthorized = false;
    },

    setUser(state, data) {
      state.user = data;
    },

    unsetUser(state) {
      state.user = {};
    },
  },
};
