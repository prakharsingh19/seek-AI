import NavBar from "../components/navBar.js";
import RightSideBar from "../components/RightSideBar.js";

export default {
    components: { NavBar, RightSideBar },
    template: `
    <div>
        <NavBar />
        <div class="profilePageContainer" style="display: flex; padding: 30px; background-color: #f8f9fa; min-height: 100vh;">
            <RightSideBar />

            <div class="profilePageMain" style="flex-grow: 1; margin-left: 30px; background-color: #ffffff; padding: 30px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); transition: all 0.3s ease;">
                <h1 class="profilePageTitle" style="text-align: center; color: #2c3e50; margin-bottom: 30px; font-weight: 600; font-size: 2.2rem;">My Profile</h1>

                <!-- Profile Card -->
                <div class="profilePageCard" style="display: flex; align-items: center; margin-bottom: 30px; padding: 25px; background: linear-gradient(145deg, #ffffff, #f8f9fa); border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: transform 0.2s ease; cursor: pointer;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
                    <img src="https://img.freepik.com/premium-photo/male-female-profile-avatar-user-avatars-gender-icons_1020867-74966.jpg"
                        class="profilePageAvatar" alt="Student Photo" style="width: 120px; height: 120px; border-radius: 50%; margin-right: 30px; border: 4px solid #fff; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                    <div class="profilePageInfo" style="flex-grow: 1;">
                        <h3 style="margin: 0; color: #2c3e50; font-size: 1.8rem; font-weight: 600;">{{ userName }}</h3>
                        <p style="margin: 8px 0; color: #6c757d; font-size: 1.1rem;">Level: <span style="color: #3498db; font-weight: 500;">{{ userLevel }}</span></p>
                        <p style="margin: 8px 0; color: #6c757d; font-size: 1.1rem;">DOB: <span style="color: #3498db; font-weight: 500;">{{ userDOB }}</span></p>
                    </div>
                </div>

                <!-- Badges -->
                <div class="profilePageBadges" style="margin-bottom: 30px; background: #fff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <h5 style="color: #2c3e50; margin-bottom: 15px; font-size: 1.3rem; font-weight: 600;">Achievements & Badges</h5>
                    <div class="badgesContainer" style="display: flex; flex-wrap: wrap; gap: 12px;">
                        <span v-for="badge in userBadges" :key="badge" class="profilePageBadge" :class="badgeClass(badge)" 
                            style="padding: 8px 16px; border-radius: 25px; font-size: 1rem; color: #ffffff; font-weight: 500; letter-spacing: 0.5px; transition: all 0.3s ease; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.1);" 
                            onmouseover="this.style.transform='scale(1.05)'" 
                            onmouseout="this.style.transform='scale(1)'">
                            {{ badge }}
                        </span>
                    </div>
                </div>

                <!-- Accordion Sections -->
                <div class="accordion profilePageAccordion" id="profileAccordion" style="margin-bottom: 30px;">
                    <!-- Projects -->
                    <div class="accordion-item" style="margin-bottom: 15px; border: none;">
                        <h2 class="accordion-header">
                            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#projectsSection"
                                style="background-color: #ffffff; color: #2c3e50; border: 1px solid #e9ecef; border-radius: 12px; padding: 15px 20px; font-weight: 600; font-size: 1.1rem; transition: all 0.3s ease;">
                                Projects
                            </button>
                        </h2>
                        <div id="projectsSection" class="accordion-collapse collapse show">
                            <div class="accordion-body" style="padding: 20px; background-color: #ffffff; border: 1px solid #e9ecef; border-top: none; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;">
                                <p v-for="(project, index) in userProjects" :key="index" style="color: #2c3e50; margin-bottom: 10px; font-size: 1.1rem;">{{ project }}</p>
                                <button class="btn btn-primary" style="background-color: #3498db; border: none; color: white; font-weight: 600; border-radius: 8px; padding: 10px 20px; margin-top: 15px; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='#2980b9'" onmouseout="this.style.backgroundColor='#3498db'">Edit</button>
                            </div>
                        </div>
                    </div>

                    <!-- Address -->
                    <div class="accordion-item">
                        <h2 class="accordion-header">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#addressSection"
                                style="background-color: #ffffff; color: #343a40; border: 1px solid #dee2e6; border-radius: 8px; margin-bottom: 10px;">
                                Address
                            </button>
                        </h2>
                        <div id="addressSection" class="accordion-collapse collapse">
                            <div class="accordion-body" style="padding: 15px; background-color: #ffffff; border: 1px solid #dee2e6; border-top: none; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;">
                                <p>{{ userAddress }}</p>
                                <button class="btn btn-primary" style="background-color: #007bff; border-color: #007bff; color: white; font-weight: 600; border-radius: 5px; padding: 8px 15px; margin-top: 10px;">Edit</button>
                            </div>
                        </div>
                    </div>

                    <!-- Personal Links -->
                    <div class="accordion-item">
                        <h2 class="accordion-header">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#linksSection"
                                style="background-color: #ffffff; color: #343a40; border: 1px solid #dee2e6; border-radius: 8px; margin-bottom: 10px;">
                                Personal Links
                            </button>
                        </h2>
                        <div id="linksSection" class="accordion-collapse collapse">
                            <div class="accordion-body" style="padding: 15px; background-color: #ffffff; border: 1px solid #dee2e6; border-top: none; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;">
                                <p>LinkedIn: <a :href="userLinks.linkedin" target="_blank">{{ userLinks.linkedin }}</a></p>
                                <p>GitHub: <a :href="userLinks.github" target="_blank">{{ userLinks.github }}</a></p>
                                <button class="btn btn-primary" style="background-color: #007bff; border-color: #007bff; color: white; font-weight: 600; border-radius: 5px; padding: 8px 15px; margin-top: 10px;">Edit</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Logout Button -->
                <button class="profilePageLogoutBtn" @click="logout" 
                    style="display: block; width: 100%; padding: 12px; background-color: #e74c3c; color: #ffffff; border: none; border-radius: 12px; cursor: pointer; margin-top: 30px; font-size: 1.1rem; font-weight: 600; transition: all 0.3s ease; box-shadow: 0 4px 6px rgba(231, 76, 60, 0.2);"
                    onmouseover="this.style.backgroundColor='#c0392b'; this.style.transform='translateY(-2px)'" 
                    onmouseout="this.style.backgroundColor='#e74c3c'; this.style.transform='translateY(0)'">
                    Logout
                </button>
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            userName: this.$store.state.name || "Student Name",
            userLevel: "Degree/Foundation/Diploma",
            userDOB: "July 13, 2099",
            userBadges: ["Python Expert", "Full Stack Developer", "AI Enthusiast", "Data Science", "Machine Learning"],
            userProjects: ["Project 1: XYZ", "Project 2: ABC"],
            userAddress: "123, Street Name, City, State",
            userLinks: {
                linkedin: "https://linkedin.com/yourprofile",
                github: "https://github.com/yourprofile"
            }
        };
    },
    methods: {
        badgeClass(badge) {
            const colors = ["bg-primary", "bg-success", "bg-warning text-dark", "bg-danger", "bg-info text-dark", "bg-secondary", "bg-dark", "bg-light text-dark"];
            return colors[Math.floor(Math.random() * colors.length)];
        },
        logout() {
            this.$store.commit("logout");
            this.$router.push("/login");
        }
    }
};