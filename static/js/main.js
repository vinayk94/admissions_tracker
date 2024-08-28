document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");

    // Existing smooth scrolling code
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Existing form validation code
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            const requiredFields = form.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value) {
                    event.preventDefault();
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
        });
    }

    // New code for toggling filters and form
    const toggleFilters = document.getElementById('toggle-filters');
    const toggleForm = document.getElementById('toggle-form');
    
    console.log("Toggle Filters button:", toggleFilters);
    console.log("Toggle Form button:", toggleForm);

    if (toggleFilters) {
        toggleFilters.addEventListener('click', function() {
            console.log("Filters button clicked");
            const filtersContainer = document.getElementById('filters-container');
            console.log("Filters container:", filtersContainer);
            if (filtersContainer) {
                filtersContainer.style.display = filtersContainer.style.display === 'none' ? 'block' : 'none';
                console.log("Filters container display:", filtersContainer.style.display);
            }
        });
    }

    if (toggleForm) {
        toggleForm.addEventListener('click', function() {
            console.log("Form button clicked");
            const formContainer = document.getElementById('form-container');
            console.log("Form container:", formContainer);
            if (formContainer) {
                formContainer.style.display = formContainer.style.display === 'none' ? 'block' : 'none';
                console.log("Form container display:", formContainer.style.display);
            }
        });
    }
});