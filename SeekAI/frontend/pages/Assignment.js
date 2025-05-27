import NavBar from "../components/navBar.js";
import RightSideBar from "../components/RightSideBar.js";

export default {
  components: { NavBar, RightSideBar },
  props: ["course_id", "week_number"],
  data() {
    return {
      assignments: [],
      questions: [],
      choices: {},
      selectedChoices: {},
      hints: {},
      successMessage: "", // Stores success message after submission
    };
  },
  mounted() {
    console.log("Course ID:", this.course_id);
    console.log("Week Number:", this.week_number);
    console.log("Auth Token:", this.$store.state.auth_token);
    this.fetchAssignments();
  },
  methods: {
    async fetchAssignments() {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/courses/${this.course_id}/weeks/${this.week_number}/assignments`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${this.$store.state.auth_token}`,
            },
          }
        );

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        this.assignments = await response.json();
        if (this.assignments.length > 0) {
          this.fetchQuestions(this.assignments[0].assignment_id);
        }
      } catch (error) {
        console.error("Error fetching assignments:", error);
      }
    },

    async fetchQuestions(assignmentId) {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/assignments/${assignmentId}/questions`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${this.$store.state.auth_token}`,
            },
          }
        );

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        this.questions = await response.json();

        this.questions.forEach((question, index) => {
          this.fetchChoices(question.question_id);
          this.$set(question, "serial_no", index + 1);
        });
      } catch (error) {
        console.error("Error fetching questions:", error);
      }
    },

    async fetchChoices(questionId) {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/questions/${questionId}/choices`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${this.$store.state.auth_token}`,
            },
          }
        );

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        this.$set(this.choices, questionId, await response.json());
      } catch (error) {
        console.error(`Error fetching choices for question ${questionId}:`, error);
      }
    },

    async fetchHint(questionStmt, questionId) {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/question_hint/${encodeURIComponent(questionStmt)}`,
          {
            method: "GET",
          }
        );

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();
        this.$set(this.hints, questionId, data.hint);
      } catch (error) {
        console.error(`Error fetching hint for question ${questionId}:`, error);
      }
    },

    async submitAssignment() {
      try {
        if (this.assignments.length === 0) {
          alert("No assignment available to submit.");
          return;
        }

        const assignmentId = this.assignments[0].assignment_id;

        const response = await fetch(
          `http://127.0.0.1:5000/api/assignments/${assignmentId}/submission`,
          {
            method: "PUT",
            headers: {
              Authorization: `Bearer ${this.$store.state.auth_token}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ marks_obtained: null }),
          }
        );

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const result = await response.json();

        // Store the success message
        this.successMessage = `The assignment was successfully submitted on ${new Date().toLocaleString()}, and your score is ${result.marks_obtained}.`;

      } catch (error) {
        console.error("Error submitting assignment:", error);
        this.successMessage = "There was an error submitting your assignment.";
      }
    },
  },

  template: `
    <div>
      <NavBar />
      <div class="container mt-5" style="margin-top: 80px; padding: 20px;">
        <h2 class="text-center"> Assignment - Week {{ week_number }}</h2>

        <!-- Success Message -->
        <p v-if="successMessage" class="alert alert-success text-center">
          {{ successMessage }}
        </p>

        <div class="mt-4">
          <h3>Questions</h3>
          <div v-if="questions.length === 0" class="text-muted">No questions available.</div>
          
          <div v-for="question in questions" :key="question.question_id" class="card p-3 mt-3">
            <div class="d-flex justify-content-between align-items-center">
              <p><strong>{{ question.serial_no }}.</strong> {{ question.stmt }}</p>
              <button class="btn btn-sm btn-success" @click="fetchHint(question.stmt, question.question_id)">Hint</button>
            </div>
            
            <p v-if="hints[question.question_id]" class="text-success">Hint: {{ hints[question.question_id] }}</p>
            
            <div v-if="choices[question.question_id] && choices[question.question_id].length > 0">
              <div v-for="choice in choices[question.question_id]" :key="choice.choice_id">
                <input type="radio" :name="'question_' + question.question_id" :value="choice.choice_id" v-model="selectedChoices[question.question_id]">
                {{ choice.choice_stmt }}
              </div>
            </div>
            <div v-else class="text-muted">No choices available.</div>
          </div>
        </div>
        
        <button class="btn btn-success mt-4" @click="submitAssignment">Submit</button>
      </div>
      
      <RightSideBar />
    </div>
  `,
};
