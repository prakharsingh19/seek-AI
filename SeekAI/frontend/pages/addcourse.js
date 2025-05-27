export default {
    template: `
      <div class="register-container">
          <div class="register-box">
              <div class="register-title-section">
                  <img src="assets/logo.png" alt="seek.AI Logo" class="register-logo" />
                  <h2 class="register-title">ADD NEW COURSE</h2>
              </div>
  
              <form @submit.prevent="submitaddcourse">
                  <div class="register-form-content">
                      <!-- Left Section (Common Fields) -->
                      <div class="register-left-section">
                        <input type="text" v-model="name" class="register-form-control" placeholder="Course Name" required />
                        <input type="text" v-model="desc" class="register-form-control" placeholder="Course Description" required />
                        <input type="text" v-model="course_code" class="register-form-control" placeholder="Course Code" required />
                        <input type="text" v-model="term_name" class="register-form-control" placeholder="Term Name" required />
  
                             
  
                  <button type="submit" class="register-btn-register">Submit</button>
  
                  <p v-if="alertMessage" class="register-error-message">{{ alertMessage }}</p>
                  
              </form>
          </div>
      </div>
    `,
    userData() {
        return {
            name: "",
            desc: "",
            term_name: "",
            course_code: "",

        };
    },
    methods: {
        async submitaddcourse() {
            console.log("started adding");

            try {
                const userData = JSON.parse(localStorage.getItem("user"));
                const token = userData.token;
                console.log(token);
                //if (!userData || !userData.token) {
                //console.error("Token not found. Please log in again.");
                //this.$router.push("/admin-dashboard");

                const res = await fetch(`${location.origin}/api/course`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}`, },
                    body: JSON.stringify({
                        name: this.name,
                        desc: this.desc,
                        term_name: this.term_name,
                        course_code: this.course_code,

                    }),
                });

                if (res.ok) {
                    const data = await res.json();
                    this.alertMessage = "Course added.";

                    setTimeout(() => {
                        if (this.$store.state.role.includes("admin")) {
                            this.$router.push("/admin-dashboard");
                        }
                    }, 1000);
                } else {
                    const errorData = await res.json();
                    this.alertMessage = errorData.message || "Course already exists.";
                }
            } catch (error) {
                this.alertMessage = "Something went wrong.";
            }
        },
    },
};
