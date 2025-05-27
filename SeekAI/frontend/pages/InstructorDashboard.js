import NavBar from "../components/navBar.js";
import RightSideBar from "../components/RightSideBar.js";

export default {
  components: { NavBar, RightSideBar },
  template: `
    <div>
        <NavBar />
        <div class="instructor-dashboard" style="display: flex; height: calc(100vh - 60px);">
            <!-- Left Sidebar -->
            <aside style="width: 250px; background-color: #f0f0f0; padding: 20px;">
                <div style="margin-bottom: 20px;">
                    <h2>Welcome, {{ userName }}</h2>
                    <p style="color: #6c757d;">{{ userRole }}</p>
                </div>
                <div style="margin-bottom: 20px;">
                    <input type="text" placeholder="Search Courses..." style="width: 100%; padding: 8px; margin-bottom: 5px; border-radius: 4px; border: 1px solid #dee2e6;">
                    <button style="width: 100%; padding: 8px; background-color: #007bff; color: white; border: none; border-radius: 4px;">Filter</button>
                </div>
                <div>
                    <h3>My Courses</h3>
                    <div v-for="course in courses" :key="course.course_id" 
                        style="margin-bottom: 5px; cursor: pointer; padding: 8px; border-radius: 4px; transition: all 0.3s ease;"
                        :style="{ backgroundColor: selectedCourse && selectedCourse.course_id === course.course_id ? '#007bff' : 'transparent',
                                color: selectedCourse && selectedCourse.course_id === course.course_id ? 'white' : '#333' }"
                        @click="selectCourse(course)">
                        {{ course.name }}
                    </div>
                </div>
                <button @click="addNewModule" style="width: 100%; padding: 8px; background-color: #28a745; color: white; border: none; border-radius: 4px; margin-top: 20px;">Add New Module</button>
                <button @click="addAssignment" style="width: 100%; padding: 8px; background-color: #17a2b8; color: white; border: none; border-radius: 4px; margin-top: 10px;">Manage Assignments</button>
            </aside>

            <!-- Main Content -->
            <main style="flex-grow: 1; padding: 20px; overflow-y: auto;">
                <div v-if="selectedCourse" style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h2>{{ selectedCourse.name }}</h2>
                    <p style="color: #6c757d;">{{ selectedCourse.desc }}</p>
                </div>

                <!-- Modules Section -->
                <div style="margin-top: 20px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3>Weeks</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="background-color: #f8f9fa;">
                                <th style="padding: 12px; text-align: left; border-bottom: 2px solid #dee2e6;">Week Number</th>
                                <th style="padding: 12px; text-align: right; border-bottom: 2px solid #dee2e6;">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="week in weeks" :key="week.week_id" style="border-bottom: 1px solid #dee2e6;">
                                <td style="padding: 12px;">week {{ week.week_id }}</td>
                                <td style="padding: 12px; text-align: right;">
                                    <button @click="editModule(week)" style="background-color: #ffc107; color: white; border: none; padding: 6px 12px; border-radius: 4px; margin-right: 8px;">Edit</button>
                                    <button @click="addVideo(week.week_id)" style="background-color: #ffc107; color: white; border: none; padding: 6px 12px; border-radius: 4px; margin-right: 8px;">Add video</button>
                                    <button @click="deleteModule(week)" style="background-color: #dc3545; color: white; border: none; padding: 6px 12px; border-radius: 4px;">Delete</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <button @click="addNewModule" style="background-color: #28a745; color: white; border: none; padding: 8px 16px; border-radius: 4px; margin-top: 16px;">Add Week</button>
                </div>

                <!-- Assignments Section -->
                <div style="margin-top: 20px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3>Assignments</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="background-color: #f8f9fa;">
                                <th style="padding: 12px; text-align: left; border-bottom: 2px solid #dee2e6;">Assignment Name</th>
                                <th style="padding: 12px; text-align: right; border-bottom: 2px solid #dee2e6;">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="assignment in assignments" :key="assignment.assignment_id" style="border-bottom: 1px solid #dee2e6;">
                                <td style="padding: 12px;">Assignment {{ assignment.assignment_id }}</td>
                                <td style="padding: 12px; text-align: right;">
                                    <button @click="editAssignment(assignment)" style="background-color: #ffc107; color: white; border: none; padding: 6px 12px; border-radius: 4px; margin-right: 8px;">Edit</button>
                                    <button @click="addQuestion(assignment)" style="background-color: #ffc107; color: white; border: none; padding: 6px 12px; border-radius: 4px; margin-right: 8px;">Add question</button>
                                    <button @click="deleteAssignment(assignment)" style="background-color: #dc3545; color: white; border: none; padding: 6px 12px; border-radius: 4px;">Delete</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <button @click="addAssignment" style="background-color: #28a745; color: white; border: none; padding: 8px 16px; border-radius: 4px; margin-top: 16px;">Add Assignment</button>
                </div>
            </main>

            <!-- Right Sidebar -->
            <RightSideBar />
        </div>
    </div>
    `,
  // Inside data() function
  data() {
    return {
      courses: [],
      selectedCourse: null,
      weeks: [
        // Example structure after fetch:
        // { week_id: 1, week_no: 1, course_id: 10, videos: null, loadingVideos: false, fetchError: null },
      ],
      assignments: [],
      instructorId: null, // Make sure this is being set correctly (e.g., in mounted)
      expandedWeekId: null, // ID of the currently expanded week
    };
  },
  computed: {
    userName() {
      return this.$store.state.name || "Instructor";
    },
    userRole() {
      return this.$store.state.role || "Instructor";
    },
  },
  methods: {
    selectCourse(course) {
      this.selectedCourse = course;
      this.fetchModulesAndAssignments(course.course_id);
    },
    async fetchModulesAndAssignments(courseId) {
      try {
        const token = JSON.parse(localStorage.getItem("user")).token;
        const [modulesResponse, assignmentsResponse] = await Promise.all([
          fetch(`/api/courses/${courseId}/weeks`, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }),
          fetch(`/api/courses/${courseId}/assignments`, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }),
        ]);

        if (modulesResponse.ok && assignmentsResponse.ok) {
          this.weeks = await modulesResponse.json();
          this.assignments = await assignmentsResponse.json();
        }
      } catch (error) {
        console.error("Error fetching course data:", error);
      }
    },
    async fetchInstructorCourses() {
      try {
        const token = JSON.parse(localStorage.getItem("user")).token;
        const response = await fetch(`/api/courses`, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
        if (response.ok) {
          this.courses = await response.json();
          if (this.courses.length > 0) {
            this.selectCourse(this.courses[0]);
          }
        }
      } catch (error) {
        console.error("Error fetching instructor courses:", error);
      }
    },
    async addNewModule() {
      if (!this.selectedCourse) {
        alert("Please select a course first.");
        return;
      }
      const name = prompt("Enter module name:");
      const weekNo = prompt("Enter week number:");
      if (name && weekNo) {
        try {
          const token = JSON.parse(localStorage.getItem("user")).token;
          const response = await fetch(
            `/api/courses/${this.selectedCourse.course_id}/weeks`,
            {
              method: "POST",
              headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ name, week_no: parseInt(weekNo) }),
            }
          );
          if (response.ok) {
            await this.fetchModulesAndAssignments(
              this.selectedCourse.course_id
            );
          } else {
            const error = await response.json();
            alert(error.message);
          }
        } catch (error) {
          console.error("Error adding module:", error);
        }
      }
    },
    async editModule(module) {
      const newName = prompt("Edit module name:", module.name);
      const newWeekNo = prompt("Edit week number:", module.week_no);
      if (newName !== null && newWeekNo !== null) {
        try {
          const token = JSON.parse(localStorage.getItem("user")).token;
          const response = await fetch(`/api/weeks/${module.week_id}`, {
            method: "PUT",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              name: newName,
              week_no: parseInt(newWeekNo),
            }),
          });
          if (response.ok) {
            await this.fetchModulesAndAssignments(
              this.selectedCourse.course_id
            );
          } else {
            const error = await response.json();
            alert(error.message);
          }
        } catch (error) {
          console.error("Error updating module:", error);
        }
      }
    },
    async deleteModule(module) {
      if (confirm("Are you sure you want to delete this module?")) {
        try {
          const token = JSON.parse(localStorage.getItem("user")).token;
          const response = await fetch(`/api/weeks/${module.week_id}`, {
            method: "DELETE",
            headers: { Authorization: `Bearer ${token}` },
          });
          if (response.ok) {
            await this.fetchModulesAndAssignments(
              this.selectedCourse.course_id
            );
          } else {
            const error = await response.json();
            alert(error.message);
          }
        } catch (error) {
          console.error("Error deleting module:", error);
        }
      }
    },
    async addVideo(weekId) {
      // weekId is now correctly the ID number
      const videoUrl = prompt("Enter video URL:");
      if (videoUrl !== null && videoUrl.trim() !== "") {
        const videoNo = prompt("Enter video number:");
        if (videoNo !== null && !isNaN(parseInt(videoNo))) {
          const title = prompt("Enter video title:");
          if (title !== null && title.trim() !== "") {
            const transcript = prompt("Enter video transcript (optional):");
            const tags = prompt("Enter video tags (optional):");

            try {
              const token = JSON.parse(localStorage.getItem("user")).token;
              const response = await fetch("/api/videos", {
                // Ensure '/api' prefix if needed
                method: "POST",
                headers: {
                  Authorization: `Bearer ${token}`,
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({
                  // CHANGE THIS LINE: Use weekId directly
                  week_id: weekId,
                  // END CHANGE
                  video_no: parseInt(videoNo),
                  title: title,
                  video_url: videoUrl,
                  transcript: transcript || "",
                  tags: tags || "",
                }),
              });

              if (response.ok) {
                alert("Video added successfully!"); // Give feedback
                // You likely want to refresh the view or video list here.
                // If you need to see videos per week, you might need a fetchVideosForWeek function
                // or simply refetch all modules/assignments if that implicitly updates videos.
                // For now, let's assume refetching the course data is sufficient:
                if (this.selectedCourse) {
                  // Maybe fetch videos specifically? Or refetch everything?
                  // Example: Re-fetch modules and assignments (assuming videos are nested or related)
                  // await this.fetchModulesAndAssignments(this.selectedCourse.course_id);
                  // Or, if you have a specific function to fetch just videos for this week/course:
                  // await this.fetchVideosForWeek(weekId);
                  // Simple approach if videos aren't displayed directly in the main tables:
                  // No explicit refresh needed here, just the success alert.
                }
              } else {
                const error = await response.json();
                // Check for 405 specifically, though it should now be gone or be 400/500
                if (response.status === 405) {
                  alert(
                    `Error: Method Not Allowed. Check API route configuration for POST /api/videos. (${error.message})`
                  );
                } else {
                  alert(
                    `Error adding video: ${
                      error.message || response.statusText
                    }`
                  );
                }
              }
            } catch (error) {
              console.error("Error adding video:", error);
              alert("An error occurred while adding the video.");
            }
          } else {
            alert("Title is required.");
          }
        } else {
          alert("Video number must be a number.");
        }
      } else {
        alert("Video URL is required.");
      }
    },
    async addAssignment() {
      if (!this.selectedCourse) {
        alert("Please select a course first.");
        return;
      }
      // Use this.instructorId which is set in mounted()
      if (!this.instructorId) {
        alert("Instructor ID not found. Please log in again.");
        return; // Or handle appropriately
      }

      const weekNo = prompt("Enter week number:");
      // Make the prompt very specific about the required format
      const dueDate = prompt(
        "Enter due date exactly in YYYY-MM-DD HH:MM:SS format:"
      );

      // Basic validation for prompt cancellation or empty input
      if (
        weekNo === null ||
        dueDate === null ||
        weekNo.trim() === "" ||
        dueDate.trim() === ""
      ) {
        alert("Week number and due date cannot be empty.");
        return;
      }

      const weekNoInt = parseInt(weekNo);
      if (isNaN(weekNoInt)) {
        alert("Invalid week number. Please enter a number.");
        return;
      }

      try {
        const token = JSON.parse(localStorage.getItem("user")).token;
        // const instructorId = 5; // REMOVE THIS HARDCODED VALUE
        // console.log(instructorId) // REMOVE THIS

        const response = await fetch("/api/assignments", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            week_no: weekNoInt, // Send parsed integer
            course_id: this.selectedCourse.course_id,
            due_date: dueDate, // Send the string from the prompt
            instructor_id: 5, // USE THE CORRECT INSTRUCTOR ID
          }),
        });

        if (response.ok) {
          await this.fetchModulesAndAssignments(this.selectedCourse.course_id);
          alert("Assignment added successfully!"); // Optional: Provide feedback
        } else {
          const error = await response.json();
          // Display the specific error from the backend (e.g., date format error)
          alert(`Error adding assignment: ${error.message || "Unknown error"}`);
          console.error("Server response:", error); // Log the full error
        }
      } catch (error) {
        console.error("Error adding assignment:", error);
        alert("An unexpected error occurred while adding the assignment.");
      }
    },
    async addQuestion(assignment) {
      const question = prompt("Enter question:");
      const option1 = prompt("Enter option 1:");
      const option2 = prompt("Enter option 2:");
      const option3 = prompt("Enter option 3:");
      const option4 = prompt("Enter option 4:");
      const rightOption = prompt("Enter the correct option (1-4):");

      if (question !== null) {
        try {
          const token = JSON.parse(localStorage.getItem("user")).token;
          const response = await fetch(
            `/api/questions/${assignment.assignment_id}`,
            {
              method: "POST",
              headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                assignment_id: assignment.assignment_id,
                stmt: question,
                optionsStmt: `${option1}, ${option2}, ${option3}, ${option4}, ${rightOption}`,
              }),
            }
          );
          if (response.ok) {
            await this.fetchModulesAndAssignments(
              this.selectedCourse.course_id
            );
          } else {
            const error = await response.json();
            alert(error.message);
          }
        } catch (error) {
          console.error("Error adding question:", error);
        }
      }
    },

    async editAssignment(assignment) {
      const newWeekNo = prompt("Edit week number:", assignment.week_no);
      const newDueDate = prompt(
        "Edit due date (YYYY-MM-DD HH:MM:SS):",
        assignment.due_date
      );
      if (newWeekNo !== null && newDueDate !== null) {
        try {
          const token = JSON.parse(localStorage.getItem("user")).token;
          const response = await fetch(
            `/api/assignments/${assignment.assignment_id}`,
            {
              method: "PUT",
              headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                week_no: parseInt(newWeekNo),
                due_date: newDueDate,
                course_id: this.selectedCourse.course_id,
                instructor_id: JSON.parse(localStorage.getItem("user")).user_id,
              }),
            }
          );
          if (response.ok) {
            await this.fetchModulesAndAssignments(
              this.selectedCourse.course_id
            );
          } else {
            const error = await response.json();
            alert(error.message);
          }
        } catch (error) {
          console.error("Error updating assignment:", error);
        }
      }
    },
    async deleteAssignment(assignment) {
      if (confirm("Are you sure you want to delete this assignment?")) {
        try {
          const token = JSON.parse(localStorage.getItem("user")).token;
          const response = await fetch(
            `/api/assignments/${assignment.assignment_id}`,
            {
              method: "DELETE",
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          if (response.ok) {
            await this.fetchModulesAndAssignments(
              this.selectedCourse.course_id
            );
          } else {
            const error = await response.json();
            alert(error.message);
          }
        } catch (error) {
          console.error("Error deleting assignment:", error);
        }
      }
    },
  },

  mounted() {
    this.instructorId = 7;
    this.fetchInstructorCourses();
  },
};
