export default {
    template: `
    <div class="right-sidebar" :class="{ 'right-sidebar-open': isOpen }">
        <nav>
            <router-link to="/" @click="closeSidebar">Home</router-link>
            <router-link to="/profile" @click="closeSidebar">Profile</router-link>
            <router-link to="/current-courses" @click="closeSidebar">Courses</router-link>
        </nav>

        <!-- Logout Button (Always at Bottom) -->
        <button class="logout-button" @click="logout">Logout</button>
    </div>
    `,
    props: ["isOpen"],
    computed: {
        userRole() {
            const user = JSON.parse(localStorage.getItem("user"));
            return user ? user.user.roles[0] : null; // Get first role
        }
    },
    methods: {
        closeSidebar() {
            this.$emit("close-sidebar");
        },
        logout() {
            localStorage.removeItem("user"); // Remove user data
            this.$store.commit("logout"); // Reset Vuex store
            this.$router.push("/login"); // Redirect to login
        }
    }
};
