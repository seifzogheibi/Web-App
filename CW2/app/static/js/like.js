// like button
document.addEventListener("click", function (event) {
    const button = event.target.closest(".like-button");
    if (button) {
        const postId = button.getAttribute("data-post-id");

        if (!postId) {
            console.error("Post ID is undefined. Check the data-post-id attribute on the button.");
            return;
        }

        // POST request to server, updating when like/unlke
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
            // dynamically update like count when clicked
            .then((data) => {
                const icon = button.querySelector("i");
                if (data.status === "liked") {
                    icon.className = "bi bi-heart-fill";
                    button.innerHTML = `<i class="${icon.className}"></i>(${data.like_count})`;
                } else if (data.status === "unliked") {
                    icon.className = "bi bi-heart";
                    button.innerHTML = `<i class="${icon.className}"></i>(${data.like_count})`;
                }
            })
            .catch((error) => {
                console.error("Error in fetch request:", error);
            });
    }
});
