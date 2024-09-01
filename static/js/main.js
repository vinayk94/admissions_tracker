document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');

    // Toggle functionality
    function toggleElement(element) {
        if (element) {
            element.style.display = element.style.display === 'none' ? 'block' : 'none';
            console.log(`Toggled element. Visible: ${element.style.display === 'block'}`);
        } else {
            console.error('Element not found');
        }
    }

    // Handling clicks on filter and form toggles
    document.getElementById('toggle-filters')?.addEventListener('click', function() {
        toggleElement(document.getElementById('filters-container'));
        document.getElementById('form-container').style.display = 'none';
    });

    document.getElementById('toggle-form')?.addEventListener('click', function() {
        toggleElement(document.getElementById('form-container'));
        document.getElementById('filters-container').style.display = 'none';
    });

    // Handling clicks on the like button
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const isAuthenticated = this.dataset.authenticated === 'true';

            if (!isAuthenticated) {
                if (confirm('You need to log in to like this post. Go to login page?')) {
                    window.location.href = `/accounts/login/?next=${encodeURIComponent(window.location.pathname)}`;
                }
                return;
            }

            fetch(`/api/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.textContent = `Like (${data.likes_count})`;
                    this.classList.toggle('liked', data.liked);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Handling clicks on the comment button
    document.querySelectorAll('.comment-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const commentsSection = document.querySelector(`.comments-section[data-post-id="${postId}"]`);
            toggleElement(commentsSection);
        });
    });

    // Handling comment form submission
    document.querySelectorAll('.comment-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const content = this.querySelector('textarea[name="content"]').value;
    
            fetch(`/api/comment/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content: content }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const commentsList = this.closest('.comments-section').querySelector('.comments-list');
                    const newComment = document.createElement('div');
                    newComment.className = 'comment';
                    newComment.dataset.commentId = data.comment_id;
                    newComment.innerHTML = `
                        <strong>${data.comment_user}</strong> (${data.comment_date}):
                        ${data.comment_content}
                        <button class="delete-comment" data-comment-id="${data.comment_id}">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    `;
                    commentsList.appendChild(newComment);
                    this.reset();
                    
                    // Update comment count
                    const commentBtn = document.querySelector(`.comment-btn[data-post-id="${postId}"]`);
                    const currentCount = parseInt(commentBtn.textContent.match(/\d+/)[0]);
                    commentBtn.textContent = `Comments (${currentCount + 1})`;
    
                    // Add event listener for the new delete button
                    newComment.querySelector('.delete-comment').addEventListener('click', deleteComment);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Function to delete a comment
    function deleteComment(e) {
        const commentId = e.target.closest('.delete-comment').dataset.commentId;
        fetch(`/api/delete_comment/${commentId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                e.target.closest('.comment').remove();
                // Update comment count
                const commentBtn = document.querySelector(`.comment-btn[data-post-id="${data.post_id}"]`);
                const currentCount = parseInt(commentBtn.textContent.match(/\d+/)[0]);
                commentBtn.textContent = `Comments (${currentCount - 1})`;
            }
        })
        .catch(error => console.error('Error:', error));
    }

    // Add event listeners for existing delete buttons
    document.querySelectorAll('.delete-comment').forEach(button => {
        button.addEventListener('click', deleteComment);
    });

    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});