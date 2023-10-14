import { listGarages } from "@/services/garages";

const getDefaultState = () => {
  return {
    garages: [],
    currentGarage: null,
  };
};

const state = getDefaultState();

export default {
  name: "garages",
  state,
  actions: {
    getGarages({ commit, getters }) {
      return listGarages().then((responseBody) => {
        const { items } = responseBody;
        commit("setGarages", items);
        if (items.length && !getters.currentGarageId) {
          commit("setCurrentGarage", items[0]);
        }
        if (!items.length) {
          commit("setCurrentGarage", null);
        }
      });
    },
  },
  getters: {
    currentGarage(state) {
      return state.currentGarage;
    },
    dropDownList(state) {
      return state.garages.filter((item) => item.id !== state.currentGarage.id);
    },
  },
  mutations: {
    setCurrentGarage(state, garage) {
      state.currentGarage = garage;
    },
    unsetCurrentGarage(state) {
      state.currentGarage = null;
    },
    setGarages(state, garages) {
      state.garages = garages;
    },
  },
};
