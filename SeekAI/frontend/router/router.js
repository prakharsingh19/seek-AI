import Home from "../pages/home.js";
import Login from "../pages/login.js";
import Register from "../pages/register.js";
import Dashboard from "../pages/dashboard.js";
import AdminDashboard from "../pages/AdminDashboard.js";
import InstructorDashboard from "../pages/InstructorDashboard.js";
import CurrentCourses from "../pages/CurrentCourses.js";
import Course from "../pages/Course.js";
import Profile from "../pages/Profile.js";
import Assignment from "../pages/Assignment.js";
import AddAssignment from "../pages/AddAssignment.js";
import AddModule from "../pages/AddModule.js";
import addcourse from "../pages/addcourse.js";   //abhi work
import editcourse from "../pages/editcourse.js";

const routes = [
  { path: "/", component: Home },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/dashboard", component: Dashboard, meta: { requiresLogin: true } },
  {
    path: "/admin-dashboard",
    component: AdminDashboard,
    meta: { requiresLogin: true, role: "admin" },
  },
  {
    path: "/instructor-dashboard",
    component: InstructorDashboard,
    meta: { requiresLogin: true, role: "instructor" },
  },
  {
    path: "/current-courses",
    component: CurrentCourses,
    meta: { requiresLogin: true, role: "student" },
  },
  {
    path: "/courses/:id",
    component: Course,
    meta: { requiresLogin: true, role: "student" },
  },
  // {
  //   path: "/assignments/:id",
  //   component: Assignment,
  //   meta: { requiresLogin: true, role: "student" },
  // },
  {
    path: "/course/:id/add-assignment",
    component: AddAssignment,
    meta: { requiresLogin: true, role: "student" },
  },
  {
    path: "/course/:id/add-module",
    component: AddModule,
    meta: { requiresLogin: true, role: "student" },
  },
  {
    path: "/profile",
    component: Profile,
    meta: { requiresLogin: true, role: ["student", "instructor"] },
  },
  {
    path: '/courses/:course_id/weeks/:week_number/assignments/:assignment_id',
    component: Assignment,
    props: true,
    meta: { requiresLogin: true, role: "student" },
  },
  { path: '/addcourse', component: addcourse }, //abhi work
  { path: '/editcourse/:course_id', component: editcourse },
];

const router = new VueRouter({
  routes,
});

// Keep your existing navigation guard but add role-based restriction
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem("user");
  const userData = isLoggedIn ? JSON.parse(localStorage.getItem("user")) : null;
  const userRole = userData ? userData.role : null;

  if (to.meta.requiresLogin && !isLoggedIn) {
    next("/login"); // Redirect if not logged in
  } else if (to.path === "/login" && isLoggedIn) {
    alert("already logged in");
    next("/dashboard"); // Prevent logged-in users from accessing login page
  } else if (to.meta.role) {
    if (
      Array.isArray(to.meta.role)
        ? !to.meta.role.includes(userRole)
        : to.meta.role !== userRole
    ) {
      alert("Access Denied! You are not authorized to view this page.");
      next(false); // back to previous page
    } else {
      next();
    }
  } else {
    next(); // Allow access if no restrictions
  }
});

export default router;
