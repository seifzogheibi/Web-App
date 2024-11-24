console.log("dashboard.js loaded");


document.getElementById("post-button").addEventListener("click", function () {
    const content = document.getElementById("post-content").value;
    if (!content.trim()) {
        alert("Post content cannot be empty!");
        return;
    }

    fetch("/create_post", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ content: content }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "success") {
                const postFeed = document.getElementById("post-feed");
                const newPost = document.createElement("div");
                newPost.classList.add("post");
                newPost.innerHTML = `
                    <p class="post-author">${data.author}</p>
                    <p class="post-timestamp">${data.timestamp}</p>
                    <p class="post-content">${data.content}</p>
                `;
                postFeed.insertBefore(newPost, postFeed.firstChild);
                document.getElementById("post-content").value = "";
            } else {
                alert("Failed to post. Please try again.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});

// Handle Like Button Click
document.addEventListener("click", function (event) {
    if (event.target.classList.contains("like-button")) {
        const postId = event.target.getAttribute("data-post-id");

        fetch("/like", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ post_id: postId }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "liked") {
                    const likeCount = document.getElementById(`like-count-${postId}`);
                    likeCount.textContent = parseInt(likeCount.textContent) + 1;
                    event.target.textContent = `Unlike (${likeCount.textContent})`;
                } else if (data.status === "unliked") {
                    const likeCount = document.getElementById(`like-count-${postId}`);
                    likeCount.textContent = parseInt(likeCount.textContent) - 1;
                    event.target.textContent = `Like (${likeCount.textContent})`;
                }
            })
            .catch((error) => console.error("Error liking post:", error));
    }
});

// Handle Comment Submission
document.addEventListener("click", function (event) {
    if (event.target.classList.contains("comment-button")) {
        const postId = event.target.getAttribute("data-post-id");
        const commentInput = event.target.previousElementSibling.value;

        fetch("/comment", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ post_id: postId, content: commentInput }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "success") {
                    const commentSection = document.getElementById(`comments-${postId}`);
                    const newComment = document.createElement("div");
                    newComment.classList.add("comment");
                    newComment.innerHTML = `
                        <p class="comment-author">${data.comment.author}</p>
                        <p class="comment-content">${data.comment.content}</p>
                        <p class="comment-timestamp">${data.comment.timestamp}</p>
                    `;
                    commentSection.appendChild(newComment);
                    event.target.previousElementSibling.value = ""; // Clear input
                } else {
                    alert(data.error || "Failed to add comment.");
                }
            })
            .catch((error) => console.error("Error adding comment:", error));
    }
});

document.addEventListener("click", function (event) {
    if (event.target.classList.contains("follow-button")) {
        const userId = event.target.dataset.userId;
        const action = event.target.textContent.trim() === "Follow" ? "follow" : "unfollow";

        fetch(`/${action}/${userId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    event.target.textContent = action === "follow" ? "Unfollow" : "Follow";
                    alert(data.message);
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error("Error:", error));
    }
});
