const store = new Vuex.Store({
    state: {
        auth_token: null,
        role: null,
        loggedIn: false,
        user_id: null,
        name: null,
    },
    mutations: {
        setUser(state) {
            try {
                const user = JSON.parse(localStorage.getItem('user'));
                if (user) {
                    state.auth_token = user.token;
                    state.role = user.role;
                    state.loggedIn = true;
                    state.user_id = user.id;
                    state.name = user.name;
                }
            } catch {
                console.warn('User not logged in');
            }
        },
        logout(state) {
            state.auth_token = null;
            state.role = null;
            state.loggedIn = false;
            state.user_id = null;
            state.name = null;
            localStorage.removeItem('user');
            setTimeout(() => location.reload(), 500);  // Delay reload to prevent flash issue
        }
    }
});

// Ensure state is initialized on page load
store.commit('setUser');
export default store;
