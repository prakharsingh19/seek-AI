import NavBar from "../components/navBar.js";
import RightSideBar from "../components/RightSideBar.js";

export default {
  components: { NavBar, RightSideBar },
  template: `<div>
    <div id="app">
      <NavBar />
      <div class="container-fluid mt-5"> 
        <div class="row">
          <!-- Sidebar -->
          <nav class="col-md-3 col-lg-2 d-md-block bg-light sidebar p-3">
            <h4>{{ name }}</h4>
            <button @click="showDetails = true; currentVideo = null; summary = ''" 
                    class="btn btn-info w-100 mb-3">
              Course Details
            </button>
            <div class="accordion" id="courseAccordion">
              <div v-for="(section, index) in weeks" :key="index" class="card">
                <div class="card-header" :id="'heading' + index">
                  <h2 class="mb-0">
                    <button class="btn btn-link" type="button" data-toggle="collapse" 
                            :data-target="'#collapse' + index" 
                            aria-expanded="true" 
                            :aria-controls="'collapse' + index">
                      {{ section.week }}
                    </button>
                  </h2>
                </div>
                <div :id="'collapse' + index" class="collapse" 
                     :aria-labelledby="'heading' + index" 
                     data-parent="#courseAccordion">
                  <div class="card-body">
                    <button v-for="(lecture, lIndex) in section.lectures" 
                            :key="lecture.id" 
                            @click="playLecture(lecture)" 
                            class="btn btn-outline-primary d-block w-100 text-left mb-2">
                      {{ lecture.title }}
                    </button>
                    <a v-for="(assignment, aIndex) in section.assignments" 
                       :key="assignment.id" 
                       :href="getAssignmentLink(assignment.week_no, assignment.id)"
                       class="btn btn-outline-primary d-block w-100 text-left mb-2">
                       Assignment {{ assignment.id }}
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </nav>
          
          <!-- Main Content -->
          <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <div v-if="showDetails || currentVideo === null" class="text-center p-5 bg-light border rounded">
              <h3>Welcome to the course: {{ name }}</h3>
              <p class="lead">Please select a lecture from the sidebar to begin.</p>
            </div>
            
            <div v-else>
              <h2>Lecture Video</h2>
              <div class="embed-responsive embed-responsive-16by9">
                <iframe class="embed-responsive-item w-100" height="400" 
                        :src="currentVideo.link" allowfullscreen></iframe>
              </div>
              
              <div class="mt-3">
                <button class="btn btn-primary">Ask seek.AI</button>
                <button class="btn btn-success" @click="fetchAISummary">AI Summary</button>
                <button class="btn btn-warning">Rate</button>
              </div>
              
              <div v-if="summary" class="alert alert-info mt-3">
                <h4>AI Summary</h4>
                <p>{{ summary }}</p>
              </div>
            </div>
          </main>
        </div>
      </div>
      <RightSideBar class="ms-3" />
    </div>
  </div>`,
  
  data() {
    return {
      name: null,
      currentVideo: null,
      selectedAssignment: null,
      selectedAnswerIndex: null,
      weeks: [],
      showDetails: true,
      course_id: null,
      summary: "",
    };
  },
  
  methods: {
    async setWeeks() {
      try {
        this.course_id = this.$route.params.id;
        if (!this.course_id) return;

        const courseDetailsResponse = await fetch(`api/courses/${this.course_id}`);
        if (courseDetailsResponse.ok) {
          const data = await courseDetailsResponse.json();
          this.name = data.name || "Course";
        }

        const courseWeeksResponse = await fetch(`api/courses/${this.course_id}/weeks`);
        if (courseWeeksResponse.ok) {
          const data = await courseWeeksResponse.json();
          for (const courseWeek of data) {
            const section = {
              week: "Week " + courseWeek.week_no,
              week_no: courseWeek.week_no,
              lectures: [],
              assignments: [],
            };

            const videoRes = await fetch(`api/courses/${this.course_id}/weeks/${courseWeek.week_no}/videos`);
            if (videoRes.ok) {
              const videos = await videoRes.json();
              for (const video of videos) {
                section.lectures.push({
                  id: video.video_id, // Store primary key
                  title: video.title,
                  link: `https://www.youtube.com/embed/${this.extractYouTubeVideoId(video.video_url)}`,
                });
              }
            }
            
            const assignmentRes = await fetch(`api/courses/${this.course_id}/weeks/${courseWeek.week_no}/assignments`);
            if (assignmentRes.ok) {
              const assignments = await assignmentRes.json();
              section.assignments = assignments.map(assignment => ({
                id: assignment.assignment_id,
                week_no: courseWeek.week_no,
              }));
            }
            this.weeks.push(section);
          }
        }
      } catch (error) {
        console.error("Error loading course data", error);
      }
    },

    async fetchAISummary() {
      if (!this.currentVideo) return;

      try {
        const response = await fetch(`/api/summarize_video/${this.currentVideo.id}`);
        if (response.ok) {
          const data = await response.json();
          this.summary = data.summary;
        } else {
          console.error("Failed to fetch summary");
        }
      } catch (error) {
        console.error("Error fetching AI summary:", error);
      }
    },
    
    extractYouTubeVideoId(url) {
      const regex = /(?:youtube\.com\/.*[?&]v=|youtu\.be\/|youtube\.com\/embed\/)([^"&?\/]*)/;
      const match = url.match(regex);
      return match ? match[1] : null;
    },
    
    getAssignmentLink(week_no, assignment_id) {
      return `#/courses/${this.course_id}/weeks/${week_no}/assignments/${assignment_id}`;
    },
    
    playLecture(lecture) {
      this.currentVideo = { link: lecture.link, id: lecture.id };
      this.showDetails = false;
      this.summary = "";
    },
  },
  
  mounted() {
    this.setWeeks();
  },
};
