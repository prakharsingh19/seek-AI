import router from "./router/router.js";
import store from "./store/store.js";
import RightSideBar from "./components/RightSideBar.js";  // Fix
import NavBar from "./components/navBar.js";  //

new Vue({
  el: "#app",
  router,
  store,
  computed: {
    isLoggedIn() {
      return this.$store.state.loggedIn;
    },
  },
  template: `
        <div>
            <navBar v-if="isLoggedIn" />
            <rightSideBar v-if="isLoggedIn" />
            <main :class="{ 'logged-in': isLoggedIn }">
                <router-view />
            </main>
        </div>
    `
});
