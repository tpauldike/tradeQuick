document.addEventListener('DOMContentLoaded', function () {
    // Get references to form and buttons
    const registrationForm = document.getElementById('registration-form');
    const registerBtn = document.getElementById('register-btn');
    const googleSignupBtn = document.getElementById('google-signup-btn');
    const facebookSignupBtn = document.getElementById('facebook-signup-btn');

    // Function to handle form submission
    const handleRegistration = async () => {
        // Collect form data
        const formData = new FormData(registrationForm);
        const urlSearchParams = new URLSearchParams(formData);
        try {
            // Make a POST request to your API endpoint
            const response = await fetch('http://localhost:5000/api/v1/users', {
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
                console.log('User registered:', user);
                // Add any additional logic for successful registration
            } else {
                const error = await response.json();
                console.error('Registration failed:', error);
                // Handle registration error
            }
        } catch (error) {
            console.error('An error occurred during registration:', error);
            // Handle general error
        }
    };

    // Function to handle Google signup
    const handleGoogleSignup = () => {
        // Add logic for Google signup
    };

    // Function to handle Facebook signup
    const handleFacebookSignup = () => {
        // Add logic for Facebook signup
    };

    // Attach event listeners
    registerBtn.addEventListener('click', handleRegistration);
    googleSignupBtn.addEventListener('click', handleGoogleSignup);
    facebookSignupBtn.addEventListener('click', handleFacebookSignup);
});

document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('password'); // Replace 'password' with the actual ID of your password input

    document.getElementById('show-password').addEventListener('change', function () {
        passwordInput.type = this.checked ? 'text' : 'password';
    });
});
