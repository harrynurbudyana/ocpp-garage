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
  actions: {},
  getters: {
    currentGarage(state) {
      return state.currentGarage;
    },
    dropDownList(state) {
      return state.garages.filter((item) => item.id !== state.currentGarage.id);
    },
  },
  mutations: {
    setCurrentGarage(state, garages) {
      if (garages.length) {
        state.currentGarage = garages[0];
      }
    },
    setCurrentGarageById(state, garageId) {
      state.currentGarage = state.garages.filter(
        (item) => item.id === garageId
      )[0];
    },
    unsetCurrentGarage(state) {
      state.currentGarage = null;
    },
    setGarages(state, garages) {
      state.garages = garages;
    },
    unsetGarages(state) {
      state.garages = [];
    },
  },
};
