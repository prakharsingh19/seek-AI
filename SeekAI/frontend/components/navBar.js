import RightSideBar from "./RightSideBar.js";
import store from "../store/store.js"; // Vuex Store for auth & role management

export default {
  components: { RightSideBar },
  template: `
    <header class="custom-navbar">
        <div class="navbar-container">
            <router-link to="/" class="custom-navbar-logo">
                <img src="/assets/logo.png" alt="seek.AI" />
            </router-link>
            <div class="custom-greeting">{{ greetingMessage }}</div>
            <div class="custom-right-section">
                <span class="custom-current-date">{{ formattedDate }}</span>
                <button v-if="isStudent" class="custom-chat-btn" @click="toggleChatbot">💬 Chat</button>
                <button class="custom-menu-btn" @click="toggleSidebar">
                    <img :src="menuIcon" alt="Menu" class="custom-menu-icon" :class="{ 'custom-rotated': isSidebarOpen }" />
                </button>
            </div>
        </div>

        <RightSideBar :isOpen="isSidebarOpen" @close-sidebar="toggleSidebar" />

        <!-- Chatbot UI -->
        <div v-if="isChatbotOpen && isStudent" class="chatbox-container">
            <div class="chatbox-header">
                Seek.AI - ChatBot
                <button @click="toggleChatbot" class="chatbox-close">❌</button>
            </div>
            <div class="chatbox-messages" ref="messageContainer">
                <div v-for="message in messages" :key="message.id" :class="['chat-message', message.sender]">
                    {{ message.text }}
                </div>
            </div>
            <div class="chatbox-input">
                <input v-model="userMessage" @keyup.enter="sendMessage" placeholder="Type a message..." />
                <button @click="sendMessage">➤</button>
            </div>
        </div>
        <div v-if="isChatbotOpen && isStudent" class="custom-overlay" @click="toggleChatbot"></div>
    </header>
  `,
  data() {
    return {
      isSidebarOpen: false,
      isChatbotOpen: false,
      menuIcon: "https://img.icons8.com/?size=100&id=30UIOfuJpZnZ&format=png&color=FFFFFF",
      formattedDate: "",
      messages: [],
      userMessage: "",
    };
  },
  computed: {
    studentName() {
      return this.$store.state.name || "Guest";
    },
    greetingMessage() {
      const hours = new Date().getHours();
      if (hours < 12) return `Good Morning, ${this.studentName}!`;
      if (hours < 18) return `Good Afternoon, ${this.studentName}!`;
      return `Good Evening, ${this.studentName}!`;
    },
    token() {
      return this.$store.state.auth_token || "";
    },
    isStudent() {
      return this.$store.state.role === "student";
    },
  },
  methods: {
    toggleSidebar() {
      this.isSidebarOpen = !this.isSidebarOpen;
    },
    toggleChatbot() {
      this.isChatbotOpen = !this.isChatbotOpen;
      if (!this.isChatbotOpen) this.messages = [];
    },
    async sendMessage() {
      if (!this.userMessage.trim()) return;

      this.messages.push({ id: Date.now(), text: this.userMessage, sender: "user" });

      try {
        const response = await fetch("http://127.0.0.1:5000/api/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": this.token, // Fetching token from Vuex store
          },
          body: JSON.stringify({ question: this.userMessage }),
        });

        console.log("Response Status:", response.status);
        console.log("Response Headers:", response.headers);

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        this.messages.push({ id: Date.now(), text: data.message, sender: "bot" });

        this.$nextTick(() => {
          this.$refs.messageContainer.scrollTop = this.$refs.messageContainer.scrollHeight;
        });

      } catch (error) {
        console.error("Error sending message:", error);
        this.messages.push({ id: Date.now(), text: "Error: SEEK.AI not responding it may possible you exeeded the limit 10 questoin in 5 min or your token has expired login again and then chat.", sender: "bot" });
      }

      this.userMessage = "";
    },
    updateDate() {
      const now = new Date();
      this.formattedDate = now.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
    },
  },
  mounted() {
    this.updateDate();
    setInterval(this.updateDate, 60000);
  },
};
