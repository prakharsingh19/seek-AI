import NavBar from "../components/navBar.js";
import RightSideBar from "../components/RightSideBar.js";

export default {
  components: { NavBar, RightSideBar },
  template: `
    <div id="app">
      <NavBar />
      
      <div class="container mt-5 d-flex"> <!-- Increased top margin -->
        <div class="flex-grow-1">
          <h2 class="text-center mb-4">My Enrolled Courses</h2>

          <div v-if="courses.length === 0" class="text-center text-muted p-5">
            <h5>You haven't enrolled in any courses yet.</h5>
            <p>Browse available courses and start learning today!</p>
            <a href="/#/all-courses" class="btn btn-outline-primary mt-3">Browse Courses</a>
          </div>

          <div class="row" v-else>
            <div v-for="course in courses" :key="course.id" class="col-lg-4 col-md-6 mb-4 d-flex">
              <div class="card shadow-sm w-100">
                <div class="card-body d-flex flex-column">
                  <h5 class="card-title mb-2">{{ course.title }}</h5>
                  <p class="card-text text-muted flex-grow-1">{{ course.description }}</p>

                  <div class="mb-2">
                    <span class="badge bg-success">Enrolled</span>
                  </div>

                  <div class="progress mb-3" style="height: 8px;">
                    <div class="progress-bar bg-primary" role="progressbar" 
                         :style="{ width: course.progress + '%' }" 
                         :aria-valuenow="course.progress" 
                         aria-valuemin="0" aria-valuemax="100">
                    </div>
                  </div>

                  <a :href="course.href" class="btn btn-primary mt-auto w-100">Go to Course</a>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <RightSideBar class="ms-3" />
      </div>
    </div>
  `,

  data() {
    return {
      courses: [],
    };
  },

  methods: {
    async setCourses() {
      try {
        const res = await fetch(`api/courses`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });

        if (res.ok) {
          const data = await res.json();
          this.courses = data.map(course => ({
            id: course.course_id,
            title: course.name,
            description: course.desc,
            image: course.image || "https://via.placeholder.com/400x200?text=Course+Image",
            href: `/#/courses/${course.course_id}`,
            progress: course.progress || Math.floor(Math.random() * 100),
          }));
          console.log(data, "enrolled courses");
        } else {
          console.log("Failed to fetch courses");
        }
      } catch (error) {
        console.log("Error while fetching courses", error);
      }
    },
  },

  mounted() {
    this.setCourses();
  },
};
