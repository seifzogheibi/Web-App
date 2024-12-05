document.addEventListener("click", function (event) {
    const button = event.target.closest(".delete-post-button");
    if (button) {
        const postId = button.getAttribute("data-post-id");

        console.log("Delete button clicked", postId);

        if (!postId) {
            console.error("Post ID is undefined. Check your button's data attributes.");
            return;
        }

        if (confirm("Are you sure you want to delete this post?")) {
            console.log("Post deletion confirmed, sending request...");

            const url = `/delete_post/${postId}?redirect_from=view_post`;

            fetch(url, {
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
                        const postElement = button.closest(".dashboard-posts-cards");
                        if (postElement) {
                            postElement.remove();
                            console.log("Post removed from the DOM");
                        }
                    } else {
                        console.error("Error deleting post:", data.error);
                        alert(data.error || "Could not delete the post.");
                    }
                })
                .catch((error) => {
                    console.error("Error deleting post:", error);
                });
        } else {
            console.log("Post deletion cancelled.");
        }
    }
});
