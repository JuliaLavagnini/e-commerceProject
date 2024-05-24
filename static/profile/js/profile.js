document.addEventListener('DOMContentLoaded', function() {
    var editButton = document.getElementById('edit-details-btn');
    var formContainer = document.getElementById('form-container');
    
    editButton.addEventListener('click', function() {
        if (formContainer.style.display === 'none' || formContainer.style.display === '') {
            formContainer.style.display = 'block';
        } else {
            formContainer.style.display = 'none';
        }
    });
});