document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const messageElement = document.getElementById('message');

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default form submission

        const username = loginForm.username.value;
        const password = loginForm.password.value;

        // Basic client-side validation
        if (username.trim() === '' || password.trim() === '') {
            messageElement.textContent = 'Please enter both username and password.';
            messageElement.style.color = 'red';
            return;
        }

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
            });

            if (response.ok) {
                // Assuming the server redirects on success, or sends a success status
                window.location.href = '../index';
            } else {
                const errorText = await response.text();
                messageElement.textContent = errorText || 'Login failed. Please try again.';
                messageElement.style.color = 'red';
            }
        } catch (error) {
            console.error('Error during login:', error);
            messageElement.textContent = 'An error occurred. Please try again later.';
            messageElement.style.color = 'red';
        }
    });
});