import store from "@/store"; // We need to import store like this here

export default (to, from, next) => {
  if (!store.getters.isAuthorized) {
    // Not-authorized user tries to reach forbidden pages => redirect to "Login" page
    next({
      name: "login",
    });
  } else {
    if (
      ["Garages", "SingleGarage"].includes(to.name) &&
      !store.getters.currentUser.is_superuser
    ) {
      next({
        name: "Stations",
        params: { garageId: store.getters.currentGarage.id },
      });
    } else {
      next();
    }
  }
};
