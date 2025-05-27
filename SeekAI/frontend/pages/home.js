export default {
  template: `
        <header class="hero" style="background: linear-gradient(135deg, #a02334, #661822); color: white; text-align: center; padding: 100px 0;">
        <div class="container">
            <h1 style="font-size: 3.5rem; margin-bottom: 20px;">Welcome to seek.AI</h1>
            <p style="font-size: 1.2rem; margin-bottom: 40px;">Unlock your potential with our comprehensive online courses.</p>
            <a href="/#/register" class="btn btn-light btn-lg">Get Started Today</a>
        </div>
    </header>

    <section class="features container py-5" style="padding: 80px 0;">
        <div class="row">
            <div class="col-md-4 mb-4">
                <div class="feature-card card p-4 h-100" style="border: none; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); transition: transform 0.3s ease;">
                    <i class="fas fa-graduation-cap" style="font-size: 2.5rem; color: #a02334; margin-bottom: 20px;"></i>
                    <h3>Expert Instructors</h3>
                    <p>Learn from industry professionals with years of experience.</p>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="feature-card card p-4 h-100" style="border: none; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); transition: transform 0.3s ease;">
                    <i class="fas fa-video" style="font-size: 2.5rem; color: #a02334; margin-bottom: 20px;"></i>
                    <h3>Interactive Lessons</h3>
                    <p>Engaging video lectures and hands-on projects.</p>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="feature-card card p-4 h-100" style="border: none; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); transition: transform 0.3s ease;">
                    <i class="fas fa-comments" style="font-size: 2.5rem; color: #a02334; margin-bottom: 20px;"></i>
                    <h3>Community Support</h3>
                    <p>Connect with fellow learners and get your questions answered.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="courses container-fluid" style="background-color: #e9ecef; padding: 80px 0;">
        <div class="container py-5">
            <h2 class="text-center mb-5">Our Popular Courses</h2>
            <div class="row">
                <div class="col-md-4 mb-4">
                    <div class="course-card card">
                        <img src="https://via.placeholder.com/400x200" class="card-img-top" alt="Course 1" style="height: 200px; object-fit: cover;">
                        <div class="card-body">
                            <h5 class="card-title">Artificial Intelligence Fundamentals</h5>
                            <p class="card-text">Learn the basics of AI and machine learning.</p>
                            <a href="#" class="btn btn-primary">Enroll Now</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 mb-4">
                    <div class="course-card card">
                        <img src="https://via.placeholder.com/400x200" class="card-img-top" alt="Course 2" style="height: 200px; object-fit: cover;">
                        <div class="card-body">
                            <h5 class="card-title">Web Development Bootcamp</h5>
                            <p class="card-text">Become a full-stack web developer in 12 weeks.</p>
                            <a href="#" class="btn btn-primary">Enroll Now</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 mb-4">
                    <div class="course-card card">
                        <img src="https://via.placeholder.com/400x200" class="card-img-top" alt="Course 3" style="height: 200px; object-fit: cover;">
                        <div class="card-body">
                            <h5 class="card-title">Data Science Essentials</h5>
                            <p class="card-text">Master data analysis and visualization techniques.</p>
                            <a href="#" class="btn btn-primary">Enroll Now</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="cta" style="background: linear-gradient(135deg, #661822, #a02334); color: white; text-align: center; padding: 80px 0;">
        <div class="container">
            <h2>Ready to Start Learning?</h2>
            <p>Join seek.AI and take your career to the next level.</p>
            <a href="/#/register" class="btn btn-light btn-lg">Sign Up Free</a>
        </div>
    </section>

    <footer class="footer" style="background-color: #343a40; color: white; text-align: center; padding: 20px 0;">
        <div class="container">
            <p>&copy; 2024 seek.AI. All rights reserved.</p>
        </div>
    </footer>
    `,
};
