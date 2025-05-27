export default {
  template: `
    <div style="display: flex; justify-content: center; align-items: center; height: 100vh; background: #ffffff;">
        <div style="width: 400px; background: rgb(233, 232, 232); padding: 30px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); text-align: center;">
            
            <!-- Logo & Title -->
            <div style="background: #a02334; color: white; padding: 20px; margin-bottom: 3vh; border-radius: 8px 8px 0 0; display: flex; flex-direction: column; align-items: center; gap: 10px;">
                <img src="assets/logo.png" alt="seek.AI Logo" style="width: 150px;">
                <h2 style="margin: 0; font-size: 22px; font-weight: bold;">Add module</h2>
            </div>

            <form @submit.prevent="submitLogin" style="display: flex; flex-direction: column; gap: 12px;">
                <input type="email" v-model="email" placeholder="Email" required 
                    style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-size: 16px;">
                
                <input type="password" v-model="password" placeholder="Password" required 
                    style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-size: 16px;">
                
                <div v-if="alertMessage" :style="{ color: alertColor, marginTop: '10px', fontSize: '14px' }">
                    {{ alertMessage }}
                </div>

                <button type="submit" 
                    style="width: 100%; padding: 12px; background-color: #a02334; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; margin-top: 10px;">
                    Login
                </button>

                <p style="margin-top: 10px;">
                    Not a user? 
                    <a href="/#/register" style="color: #a02334; text-decoration: none; font-weight: bold;">Register here</a>
                </p>
            </form>
        </div>
    </div>
    `,
  data() {
    return {
      email: "",
      password: "",
      alertMessage: null,
      alertColor: "red",
    };
  },
  methods: {
    async submitLogin() {
      try {
        const response = await fetch(`${location.origin}/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: this.email, password: this.password }),
        });

        const data = await response.json();

        if (response.ok) {
          localStorage.setItem("user", JSON.stringify(data));
          this.$store.commit("setUser", data);

          this.alertMessage = "Login successful!";
          this.alertColor = "green";

          setTimeout(() => {
            if (this.$store.state.user.roles?.includes("admin")) {
              this.$router.push("/admin-dashboard");
            } else if (this.$store.state.user.roles?.includes("instructor")) {
              this.$router.push("/instructor-dashboard");
            } else {
              this.$router.push("/dashboard");
            }
          }, 500);
        } else {
          this.alertMessage = data.message || "Login failed";
          this.alertColor = "red";
        }
      } catch (error) {
        this.alertMessage = "An error occurred. Please try again.";
        this.alertColor = "red";
      }
    },
  },
};
