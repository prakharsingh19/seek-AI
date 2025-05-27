# Seek-AI

A web application built with Vue.js (frontend) and Flask (backend) to deliver an interactive learning platform with AI-driven features.  
This was a group project done as part of the **Software Engineering course at IIT Madras**.

## 👥 Team Contributions

- **My Role (21f1006728)**: Led the development with major contributions to **database design**, **frontend setup**, and integration of **GenAI features using Retrieval-Augmented Generation (RAG)**.
- **Ruhil**: Worked on several frontend pages and was responsible for designing and implementing the **entire Flask API layer**.
- **Abhi**: Built some frontend components that connected to the API.

> 🛠️ I handled a significant part of the overall architecture and development.

## Tech Stack

### Frontend Development
- **Framework**: Vue.js (lightweight, reactive, component-based)
- **Languages**: JavaScript (ES6+), HTML5, CSS3
- **Development Tools**:
  - **VSCode**: Primary IDE with Vetur and ESLint extensions
  - **Excalidraw**: Low-fidelity wireframing
  - **Canva/Figma**: High-fidelity UI/UX prototyping

### Backend Development
- **Framework**: Flask (Python) for RESTful APIs
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **API Documentation**: Swagger/OpenAPI
- **Testing**: Pytest for unit/integration tests

### General Technologies
- **Core Language**: Python
- **Version Control**: Git (GitHub/GitLab)
- **Project Management**: Jira (Agile sprints, task tracking)

### Hosting & Deployment
- **Backend**: Render/Heroku (Flask APIs)
- **Frontend**: Netlify/Vercel (Vue.js)
- **Database**: PostgreSQL/MySQL (production), AWS RDS/Firebase (cloud options)

## Key Advantages
- **Modularity**: Component-based architecture (Vue.js/Flask)
- **Scalability**: Ready for AI/ML integration (e.g., TensorFlow)
- **Agile Development**: Jira-managed sprints with Git versioning

## Installation

### On Ubuntu/MacOS
1. Clone the repository:
   ```bash
   git clone https://github.com/21f1006728/seek-AI.git

# Setup Instructions

Follow these steps to set up and run the project:

## 1. Download the Code
Clone or download the repository to your local system.

## 2. Create a Virtual Environment
Navigate to the project folder and create a virtual environment:
```sh
python3 -m venv env
```
Or, if using Windows:
```sh
python -m venv env
```

## 3. Activate the Virtual Environment
- **Linux/macOS:**
  ```sh
  source env/bin/activate
  ```
- **Windows:**
  ```sh
  env\Scripts\activate
  ```

## 4. Install Requirements
Install the necessary dependencies:
```sh
pip install -r req.txt
```

## 5. Run the Backend
Navigate to the backend directory:
```sh
cd backend
```
Run the backend server:
```sh
python3 app.py
```

You're all set! 🚀

