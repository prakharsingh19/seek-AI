export default {
  template: `
    <div class="register-container">
        <div class="register-box">
            <div class="register-title-section">
                <img src="assets/logo.png" alt="seek.AI Logo" class="register-logo" />
                <h2 class="register-title">Register on seek.AI</h2>
            </div>

            <form @submit.prevent="submitRegister">
                <div class="register-form-content">
                    <!-- Left Section (Common Fields) -->
                    <div class="register-left-section">
                        <input type="email" v-model="email" class="register-form-control" placeholder="Email" required />
                        <input type="password" v-model="password" class="register-form-control" placeholder="Password" required />

                        <div class="register-role-selector">
                            <button 
                                type="button" 
                                class="register-role-button" 
                                :class="{ 'register-active': selectedRole === 'student' }"
                                @click="selectedRole = 'student'"
                            >
                                Student
                            </button>
                            <button 
                                type="button" 
                                class="register-role-button" 
                                :class="{ 'register-active': selectedRole === 'instructor' }"
                                @click="selectedRole = 'instructor'"
                            >
                                Instructor
                            </button>
                        </div>
                    </div>

                    <!-- Right Section (Dynamic Fields) -->
                    <div class="register-right-section">
                        <div v-if="selectedRole === 'student'" class="register-field-group">
                            <input type="text" v-model="firstname" class="register-form-control" placeholder="First Name" required />
                            <input type="text" v-model="lastName" class="register-form-control" placeholder="Last Name" required />
                            <input type="text" v-model="contactNo" class="register-form-control" placeholder="Contact Number" required />
                        </div>
                        <div v-else class="register-field-group">
                            <input type="text" v-model="fullname" class="register-form-control" placeholder="Full Name" required />
                            <input type="text" v-model="experience" class="register-form-control" placeholder="Years of Experience" required />
                            <input type="text" v-model="qualification" class="register-form-control" placeholder="Qualifications" required />
                            <input type="text" v-model="contactNo" class="register-form-control" placeholder="Contact Number" required />
                        </div>
                    </div>
                </div>

                <button type="submit" class="register-btn-register">Register</button>

                <p v-if="alertMessage" class="register-error-message">{{ alertMessage }}</p>
                <p class="login-register-text-seekai" style="margin-top: 10px">
                        Already a Registered user? 
                        <router-link to="/login" class="login-register-link-seekai">Login here</router-link>
                    </p>
            </form>
        </div>
    </div>
  `,
  data() {
    return {
      email: "",
      password: "",
      selectedRole: "student",
      first_name: "",
      last_name: "",
      contact_info: "",
      name: "",
      experience: "",
      qualification: "",
      alertMessage: "",
    };
  },
  methods: {
    async submitRegister() {
      try {
        const res = await fetch(`${location.origin}/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            role: this.selectedRole,
            ...(this.selectedRole === "student"
              ? {
                first_name: this.firstname,
                last_name: this.lastName,
                contact_info: this.contactNo,
              }
              : {
                name: this.fullname,
                experience: this.experience,
                qualification: this.qualification,
                contact_info: this.contactNo,
              }),
          }),
        });

        if (res.ok) {
          const data = await res.json();
          this.alertMessage = "Registration successful!";

          setTimeout(() => {
            this.$router.push("/login");
          }, 1000);
        } else {
          const errorData = await res.json();
          this.alertMessage = errorData.message || "Registration failed";
        }
      } catch (error) {
        this.alertMessage = "An error occurred. Please try again later.";
      }
    },
  },
};
