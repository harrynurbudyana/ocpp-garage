/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from "./App.vue";

// Composables
import { createApp } from "vue";
import { createVuetify } from "vuetify";

// Plugins
import { registerPlugins } from "@/plugins";
import "@mdi/font/css/materialdesignicons.css";

import router from "@/router";
import store from "@/store";

const vuetify = createVuetify();

const app = createApp(App);
app.use(vuetify);

registerPlugins(app);

store
  .dispatch("initAction", { isPublicPage: router.currentRoute.meta?.public })
  .then(() => {
    app.mount("#app");
    return app;
  });
