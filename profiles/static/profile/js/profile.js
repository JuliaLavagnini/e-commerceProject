document.getElementById('edit-details-btn').addEventListener('click', function() {
    var formContainer = document.getElementById('form-container');
    if (formContainer.style.display === 'none') {
        formContainer.style.display = 'block';
    } else {
        formContainer.style.display = 'none';
    }
});