import NavBar from "../components/navBar.js";
import RightSideBar from "../components/RightSideBar.js";

export default {
    components: { NavBar, RightSideBar },
    template: `
    <div>
        <!-- Navbar with logged-in user name -->
        <NavBar />

        <div class="dashboard-container">
            <div class="container mt-5 text-center">
                <h2>Welcome, {{ userName }}</h2>
                <p>Your role: <strong>{{ userRole }}</strong></p>
                <button class="btn btn-danger mt-3" @click="logout">Logout</button>
            </div>
        </div>

        <!-- Right Sidebar -->
        <RightSideBar />
    </div>
    `,
    computed: {
        userName() {
            return this.$store.state.name || "Guest";  // Get name from Vuex
        },
        userRole() {
            return this.$store.state.role || "No Role Assigned";
        }
    },
    methods: {
        logout() {
            this.$store.commit('logout');
            this.$router.push('/login');  // Redirect to login
        }
    }
};
