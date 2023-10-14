import store from "@/store"; // We need to import store like this here

export default (to, from, next) => {
  // Go to Dashboard if authorized user tries to reach public pages
  if (store.getters.isAuthorized) {
    if (!store.getters.currentUser.is_superuser) {
      next("/stations");
    } else {
      next("/garages");
    }
  } else {
    next();
  }
};
