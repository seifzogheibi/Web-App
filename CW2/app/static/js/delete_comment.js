// select all elements with delete-comment-button class
document.querySelectorAll('.delete-comment-button').forEach(button => {
    button.addEventListener('click', async (event) => {
        event.preventDefault();

        // get comment id
        const commentId = button.getAttribute('data-comment-id');
        const commentElement = button.closest('.comment'); // Target the individual comment

        // send a server-side request to execute DELETE on the retreived id
        try {
            const response = await fetch(`/delete_comment/${commentId}`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': '{{ csrf_token() }}' }
            });

            // check the request work and display a message if there are no comments
            if (response.ok) {
                commentElement.remove();

                const commentsContainer = document.querySelector('.p-3.big-comment');
                if (!commentsContainer.querySelector('.comment')) {
                    commentsContainer.innerHTML = '<p class="text-muted text-white">No comments yet. Be the first to comment!</p>';
                }
            } else {
                alert('Failed to delete the comment.');
            }
        } catch (error) {
            console.error('Error deleting comment:', error);
            alert('Something went wrong.');
        }
    });
});
