document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const sidebarToggle = document.getElementById("sidebarToggle");
    const closeSidebar = document.getElementById("closeSidebar");

    // Open Sidebar
    sidebarToggle.addEventListener("click", function () {
        sidebar.classList.toggle("open");
    });

    // Close Sidebar
    closeSidebar.addEventListener("click", function () {
        sidebar.classList.remove("open");
    });
});
