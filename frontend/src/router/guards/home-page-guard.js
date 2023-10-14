import store from "@/store"; // We need to import store like this here

export default () => {
  // Go to Dashboard or Login page from root path

  const path = store.getters.currentUser.is_superuser
    ? "/garages"
    : "/stations";
  return store.getters.isAuthorized ? path : "/login";
};
