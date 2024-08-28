document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');

    function toggleElement(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.classList.toggle('visible');
            console.log(`Toggled ${elementId}. Visible: ${element.classList.contains('visible')}`);
        } else {
            console.error(`Element with id ${elementId} not found`);
        }
    }

    const toggleFilters = document.getElementById('toggle-filters');
    const toggleForm = document.getElementById('toggle-form');

    if (toggleFilters) {
        console.log('Toggle filters button found');
        toggleFilters.addEventListener('click', function() {
            console.log('Toggle filters clicked');
            toggleElement('filters-container');
        });
    } else {
        console.error('Toggle filters button not found');
    }

    if (toggleForm) {
        console.log('Toggle form button found');
        toggleForm.addEventListener('click', function() {
            console.log('Toggle form clicked');
            toggleElement('form-container');
        });
    } else {
        console.error('Toggle form button not found');
    }

    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Like button clicked');
            const postId = this.dataset.postId;
            fetch(`/api/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                console.log('Like response:', data);
                this.textContent = `Like (${data.likes_count})`;
                if (data.authenticated) {
                    this.classList.toggle('liked', data.liked);
                } else {
                    if (confirm('You need to be logged in to like posts. Would you like to log in now?')) {
                        window.location.href = '/accounts/login/?next=' + encodeURIComponent(window.location.pathname);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        });
    });

    document.querySelectorAll('.comment-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Comment button clicked');
            const postId = this.dataset.postId;
            toggleElement(`comments-${postId}`);
        });
    });

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