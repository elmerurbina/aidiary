document.addEventListener("DOMContentLoaded", function () {
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm-password");
    const signupButton = document.getElementById("signup-button");

    const emailError = document.getElementById("email-error");
    const passwordError = document.getElementById("password-error");
    const confirmPasswordError = document.getElementById("confirm-password-error");

    function validateEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

    function validatePassword(password) {
        return password.length >= 8;
    }

    function validateConfirmPassword(password, confirmPassword) {
        return password === confirmPassword;
    }

    function updateSignupButton() {
        const isEmailValid = validateEmail(emailInput.value);
        const isPasswordValid = validatePassword(passwordInput.value);
        const isConfirmPasswordValid = validateConfirmPassword(passwordInput.value, confirmPasswordInput.value);

        if (isEmailValid && isPasswordValid && isConfirmPasswordValid) {
            signupButton.disabled = false;
        } else {
            signupButton.disabled = true;
        }
    }

    emailInput.addEventListener("input", function () {
        if (!validateEmail(emailInput.value)) {
            emailError.textContent = "Por favor ingresa una direccion de correo valida.";
        } else {
            emailError.textContent = "";
        }
        updateSignupButton();
    });

    passwordInput.addEventListener("input", function () {
        if (!validatePassword(passwordInput.value)) {
            passwordError.textContent = "Password debe tener al menos 8 caracteres.";
        } else {
            passwordError.textContent = "";
        }
        updateSignupButton();
    });

    confirmPasswordInput.addEventListener("input", function () {
        if (!validateConfirmPassword(passwordInput.value, confirmPasswordInput.value)) {
            confirmPasswordError.textContent = "Las passwords no coinciden.";
        } else {
            confirmPasswordError.textContent = "";
        }
        updateSignupButton();
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const messageContainer = document.getElementById("message-container");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    // Send message
    sendButton.addEventListener("click", function () {
        const message = userInput.value.trim();
        if (message) {
            addUserMessage(message);
            userInput.value = "";

            // Send message to the backend and get AI response
            fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message: message }),
            })
                .then((response) => response.json())
                .then((data) => {
                    addAIMessage(data.response);
                })
                .catch((error) => {
                    console.error("Error:", error);
                });
        }
    });

    // Add user message to the chat
    function addUserMessage(message) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", "user-message");
        messageElement.innerHTML = `<p>${message}</p>`;
        messageContainer.appendChild(messageElement);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

    // Add AI message to the chat
    function addAIMessage(message) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", "ai-message");
        messageElement.innerHTML = `<p>${message}</p>`;
        messageContainer.appendChild(messageElement);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }
});