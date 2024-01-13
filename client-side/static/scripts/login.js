document.addEventListener('DOMContentLoaded', function () {
    // Get references to form and buttons
    const loginForm = document.getElementById('loginForm');
    const LoginBtn = document.getElementById('login-btn');
    // Function to handle form submission
    const handleLogin = async (event) => {
        // Collect form data
        const formData = new FormData(loginForm);
        const urlSearchParams = new URLSearchParams(formData);
        try {
            // Make a POST request to your API endpoint
            const response = await fetch('http://localhost:5000/auth/user/login', {
                method: 'POST',
                body: formData,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: urlSearchParams,
            });

            // Handle the response
            if (response.ok) {
                const user = await response.json();
                console.log('User login:', user);
                // Add any additional logic for successful login
            } else {
                const error = await response.json();
                console.error('Login failed:', error);
                // Handle login error
            }
        } catch (error) {
            console.error('An error occurred during login:', error);
            // Handle general error
        }
    };

    // Attach event listener to the form
    LoginBtn.addEventListener('click', handleLogin);
});
