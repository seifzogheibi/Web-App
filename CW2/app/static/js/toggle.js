// Toggle Comments
document.addEventListener("click", function (event) {
    const button = event.target.closest(".toggle-comments-button");

    if (button) {
        const commentsContainer = button.closest(".dashboard-posts-cards").querySelector(".comments-container");

        if (commentsContainer) {
            commentsContainer.classList.toggle("hidden");

            const commentsCount = commentsContainer.querySelectorAll(".comment").length;

            button.textContent = commentsContainer.classList.contains("hidden")
                ? `View Comments (${commentsCount})`
                : "Hide Comments";
        }
    }
});




// Toggle Sidebar
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('show');
}