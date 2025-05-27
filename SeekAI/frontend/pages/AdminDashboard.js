import NavBar from "../components/navBar.js";
import RightSideBar from "../components/RightSideBar.js";

export default {
  components: { NavBar, RightSideBar },
  template: `<div>
    <div id="app" class="container-fluid">
      <div class="row">
        <!-- Sidebar -->
        <nav class="col-md-4 col-lg-3 d-md-block bg-light sidebar p-3">
          <h4>Admin Panel</h4>

          <!-- Search Bar and Add Bar -->
          <div class="form-group mb-2">
                    <input type="text" v-model="searchQuery" class="form-control" placeholder="Search by Course Name or Description" />
                    <button class="btn btn-primary mt-2" @click="searchCourses">Search</button>
                </div>
          <br><button class="btn btn-success btn-add-course btn-flash" @click="addcourse"> Add New Course</button>
          <br>
          <!-- Main Content: Course Table & Engagement Charts -->
          
          <div class="container mt-5 text-center">
        <h4>Active Courses List</h4>
        <table class="table table-striped table-bordered">
              <thead class="thead-dark">
                <tr>
                  <th>Course Name</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="course in courses" :key="course.course_id">
                  
                  
                  <td>{{ course.name }}</td>                  
                </tr>
              </tbody>
            </table>
        </nav>

        <!-- Main Content: Course Table & Engagement Charts -->
        <!-- Navbar -->
        <NavBar />
        <div class="dashboard-container">
            <div class="container mt-5 text-center">
                <h2>Admin Dashboard</h2>
                <p>Your role: <strong>{{ userRole }}</strong></p>
            </div>
           
        <!-- Main Content: Course Table & Engagement Charts -->
          
          <div class="container col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <h4>Courses List</h4>
        <table class="table table-striped table-bordered">
              <thead class="thead-dark">
                <tr>
                  <th> Course Code</th>
                  <th>Course Name</th>
                  <th>Session</th>
                  <th>Modify</th>
                  <th>Delete</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="course in courses" :key="course.course_id">
                  <td>{{ course.course_code }}</td>
                  
                  <td>{{ course.name }}</td>
                  <td>{{ course.term_name }}</td>
                  <td>
                    <button class="btn btn-success btn-edit-course" @click="editcourse(course.course_id)"> Modify</button>
                  </td>
                  <td>
                <button @click="deletecourse(course.course_id)" class="btn btn-danger btn-sm">Delete</button>
                </td>
                </tr>
              </tbody>
            </table>
            
            <div class="mt-3">
              <button class="btn btn-primary">Active Courses : {{ totalcourses }}</button>
              <button class="btn btn-success">Total Students : 10</button>
            </div>
  </div>
   
    `,
  data() {
    return {
      courses: [],
      searchQuery: "",
    };
  },
  computed: {
    userName() {
      return this.$store.state.name || "Admin"; // Fetch from Vuex
    },
    userRole() {
      return this.$store.state.role || "Administrator";
    },
  },
  created() {
    // Fetch course data when the component is mounted
    this.fetchCourses();
  },
  methods: {
    addcourse() {
      //window.location.href = "/addcourse";
      this.$router.push("/addcourse");
    },
    editcourse(course_id) {
      //window.location.href = "/addcourse";
      this.$router.push(`/editcourse/${course_id}`);
    },
    async deletecourse(course_id) {
      if (!confirm("Are you sure you want to delete this course?")) {
        return;
      }

      try {
        const token = JSON.parse(localStorage.getItem("user")).token;
        console.log(token);
        const response = await fetch(
          `${location.origin}/api/course/${course_id}`,
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        console.log("reached here");
        console.log(response);
        if (response.ok) {
          alert("Course deleted successfully.");
          this.fetchCourses(); // Refresh the course list after deletion
          this.$router.push("/admin-dashboard");
        } else {
          alert("Failed to delete the course.");
        }
      } catch (error) {
        console.error("Error deleting course:", error);
        alert("An error occurred while deleting the course.");
      }
    },
    async fetchTotalStudents() {
      try {
        // Get token from Vuex store
        const token = this.$store.state.auth_token;

        if (!token) {
          console.error("Token not found. Please log in again.");
          alert("Authentication token missing. Please log in.");
          return;
        }

        // Fetch the student list API
        const response = await fetch(`${location.origin}/api/students`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const students = await response.json();

          // Count the total number of students
          this.totalStudents = students.length;
        } else {
          console.error("Failed to fetch student data.");
          alert("Failed to load student data.");
        }
      } catch (error) {
        console.error("Error fetching students:", error);
        alert("An error occurred while fetching student data.");
      }
    },

    async fetchCourses() {
      try {
        const userData = JSON.parse(localStorage.getItem("user"));
        const token = userData ? userData.token : null;
        console.log(token);
        console.log(userData);
        //if (!userData || !userData.token) {
        //console.error("Token not found. Please log in again.");
        //this.$router.push("/admin-dashboard");

        const response = await fetch(`${location.origin}/api/courses`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          console.log(data);
          this.courses = data; // Assign fetched courses
          this.totalcourses = data.length;
        } else {
          console.error("Error fetching courses:", response.statusText);
          alert("Failed to load course data.");
        }
      } catch (error) {
        console.error("Error during API request:", error);
        alert("An error occurred while loading course data.");
      }
    },

    async searchCourses() {
      const res = await fetch(`${location.origin}/search/${this.userName}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          search: this.searchQuery,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        console.log("Search Results:", data);
        this.courses = data;
      } else {
        console.error("Error fetching search results:", res.statusText);
        alert("No courses found matching your search.");
      }
    },
  },
};
