document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const errorMessage = document.getElementById('password-error');
    errorMessage.style.display = 'none';

    form.addEventListener('submit', function (event) {
        errorMessage.style.display = 'none';

        if (!validatePasswords()) {
            event.preventDefault();
        }
    });

    function validatePasswords() {
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        if (password !== confirmPassword) {
            errorMessage.style.display = 'block';
            return false;
        }
        return true;
    }
});