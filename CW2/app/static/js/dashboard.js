// Test log to ensure the script is loaded
console.log("dashboard.js has loaded");

// Handle Like Button Click
document.addEventListener("click", function (event) {
    const button = event.target.closest(".like-button"); // Ensure correct button is targeted
    if (button) {
        const postId = button.getAttribute("data-post-id");

        if (!postId) {
            console.error("Post ID is undefined. Check the data-post-id attribute on the button.");
            return;
        }

        fetch(`/like/${postId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to like/unlike the post");
                }
                return response.json();
            })
            .then((data) => {
                const icon = button.querySelector("i"); // Keep the icon intact
                if (data.status === "liked") {
                    icon.className = "bi bi-heart-fill"; // Change to filled heart
                    button.innerHTML = `<i class="${icon.className}"></i>(${data.like_count})`;
                } else if (data.status === "unliked") {
                    icon.className = "bi bi-heart"; // Change to outlined heart
                    button.innerHTML = `<i class="${icon.className}"></i>(${data.like_count})`;
                }
            })
            .catch((error) => {
                console.error("Error in fetch request:", error);
            });
    }
});




// DETEleetere
document.addEventListener("click", function (event) {
    // Check if the clicked element or its parent is the delete button
    const button = event.target.closest(".delete-post-button");

    if (button) {
        const postId = button.getAttribute("data-post-id") || button.closest(".post-cards"); // Retrieve post ID

        if (!postId) {
            console.error("Post ID is undefined. Check your button's data attributes.");
            return;
        }

        // Confirm deletion
        if (confirm("Are you sure you want to delete this post?")) {
            // Send the delete request
            fetch(`/delete_post/${postId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Failed to delete post");
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.status === "success") {
                        const postElement = button.closest(".dashboard-posts-cards"); // Adjust the selector to match your HTML
                        if (postElement) {
                            postElement.remove(); // Remove the post dynamically
                        }
                    } else {
                        alert(data.error || "Could not delete the post.");
                    }
                })
                .catch((error) => {
                    console.error("Error deleting post:", error);
                });
        }
    }
});


// Delete Comment
document.addEventListener("click", function (event) {
    if (event.target.classList.contains("delete-comment-button")) {
        const commentId = event.target.getAttribute("data-comment-id");

        fetch(`/delete_comment/${commentId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "success") {
                    const commentElement = document.getElementById(`comment-${commentId}`);
                    commentElement.remove();
                } else {
                    alert(data.error || "Failed to delete comment.");
                }
            })
            .catch((error) => console.error("Error deleting comment:", error));
    }
});


// document.getElementById("search-toggle").addEventListener("click", function (event) {
//     event.preventDefault(); // Prevent form from submitting when clicked
//     const searchContainer = document.querySelector(".search-container");
//     searchContainer.classList.toggle("active"); // Toggle visibility
//   });
  


// Toggle Comments Section
document.addEventListener("click", function (event) {
    const button = event.target.closest(".toggle-comments-button"); // Ensure correct button is targeted
    if (button) {
        const commentsContainer = button.closest(".dashboard-posts-cards").querySelector(".comments-container");
        if (commentsContainer) {
            commentsContainer.classList.toggle("hidden"); // Toggle visibility
            // Update button text based on visibility
            button.textContent = commentsContainer.classList.contains("hidden")
                ? "View Comments"
                : "Hide Comments";
        }
    }
});



function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('hidden');
}
