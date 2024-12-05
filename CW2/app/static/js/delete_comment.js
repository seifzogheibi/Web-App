// Delete Comment
document.querySelectorAll('.delete-comment-button').forEach(button => {
    button.addEventListener('click', async (event) => {
        event.preventDefault();
        const commentId = button.getAttribute('data-comment-id');
        const commentElement = button.closest('.big-comment') || button.closest('.comment'); // Handle both Dashboard and View Post pages

        try {
            const response = await fetch(`/delete_comment/${commentId}`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': '{{ csrf_token() }}' }
            });

            if (response.ok) {
                commentElement.remove(); 
                const error = await response.json();
                alert(error.error || 'Failed to delete comment.');
            }
        } catch (error) {
            console.error('Error deleting comment:', error);
            alert('Something went wrong.');
        }
    });
});
