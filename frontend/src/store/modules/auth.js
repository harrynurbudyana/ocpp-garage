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
  router.push("/login");
}

function _processSuccessfulLogin(commit, userData) {
  commit("setAuthorized");
  commit("setUser", userData);

  if (userData.is_superuser) {
    router.push("/garages");
  } else {
    router.push("/stations");
  }
}

export default {
  name: "auth",
  state,
  actions: {
    getUser({ commit }) {
      return request.get("/me").then((responseBody) => {
        commit("setUser", responseBody);
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

    setCurrentGarageId(state, garageId) {
      state.currentGarageId = garageId;
    },
  },
};
