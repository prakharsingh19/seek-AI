export default {
    template: `
    <div class="register-container">
            <div class="register-box">
                <div class="register-title-section">
                    <img src="assets/logo.png" alt="seek.AI Logo" class="register-logo" />
                    <h2 class="register-title">EDIT COURSE</h2>
                </div>
        <form @submit.prevent="updateCourse" class="edit-form">
          <div class="form-group">
            <label>Course ID (Non-editable)</label>
            <input type="text" v-model="course.course_id" class="form-control" disabled />
          </div>
          <div class="form-group">
            <label>Course Name</label>
            <input type="text" v-model="course.name" class="form-control" required />
          </div>
          <div class="form-group">
            <label>Course Description</label>
            <input type="text" v-model="course.desc" class="form-control" required />
          </div>
          <div class="form-group">
            <label>Course Code</label>
            <input type="text" v-model="course.course_code" class="form-control" required />
          </div>
          <div class="form-group">
            <label>Term Name</label>
            <input type="text" v-model="course.term_name" class="form-control" required />
          </div>
          
          <button type="submit" class="register-btn-register">Update Course</button> 
          <br>
          <br>
          <button type="button" class="btn btn-warning" @click="$router.push('/admin-dashboard')">Cancel</button>
        </form>
      </div>
    `,
    data() {
      return {
        course: {
          course_id: "",
          name: "",
          desc: "",
          course_code: "",
          term_name: "",
        },
      };
    },
    created() {
      this.fetchCourseDetails();
    },
    methods: {
      async fetchCourseDetails() {
        const courseId = this.$route.params.course_id;
        try {
          const token = JSON.parse(localStorage.getItem("auth_token"));
          const response = await fetch(
            `${location.origin}/api/course/${courseId}`,
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          if (response.ok) {
            this.course = await response.json();
          } else {
            alert("Failed to fetch course details.");
          }
        } catch (error) {
          console.error("Error fetching course details:", error);
          alert("An error occurred while fetching course details.");
        }
      },
      async updateCourse() {
        try {
          const token = JSON.parse(localStorage.getItem("auth_token"));
          const response = await fetch(
            `${location.origin}/api/course/${this.course.course_id}`,
            {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
              body: JSON.stringify({
                name: this.course.name,
                desc: this.course.desc,
                course_code: this.course.course_code,
                term_name: this.course.term_name,
              }),
            }
          );
          if (response.ok) {
            alert("Course updated successfully.");
            this.$router.push("/admin-dashboard");
          } else {
            alert("Failed to update the course.");
          }
        } catch (error) {
          console.error("Error updating course:", error);
          alert("An error occurred while updating the course.");
        }
      },
    },
  };
  