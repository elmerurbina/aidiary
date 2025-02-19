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
    const profileForm = document.getElementById("profile-form");
    const deleteProfileButton = document.getElementById("delete-profile-button");

    // Handle profile form submission

    // Handle delete profile button click
    if (deleteProfileButton) {
        deleteProfileButton.addEventListener("click", function () {
            if (confirm("¿Estás seguro de que deseas eliminar tu perfil? Esta acción no se puede deshacer.")) {
                fetch("/delete_profile", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    }
                })
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message);
                        window.location.href = "/signin";
                    })
                    .catch(error => {
                        console.error("Error:", error);
                    });
            }
        });
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const profileForm = document.getElementById("profile-form");

    if (profileForm) {
        profileForm.addEventListener("submit", function (event) {
            let name = document.getElementById("name").value.trim();
            let email = document.getElementById("email").value.trim();
            let photo = document.getElementById("photo").value.trim();
            let password = document.getElementById("password") ? document.getElementById("password").value.trim() : "";

            console.log("Validating inputs..."); // Debugging message

            if (name.length > 255) {
                alert("El nombre no puede tener más de 255 caracteres.");
                event.preventDefault();
                return;
            }
            if (email.length > 255) {
                alert("El correo no puede tener más de 255 caracteres.");
                event.preventDefault();
                return;
            }
            if (photo.length > 255) {
                alert("La URL de la foto no puede tener más de 255 caracteres.");
                event.preventDefault();
                return;
            }
            if (password.length > 0 && password.length < 8) {
                alert("La contraseña debe tener al menos 8 caracteres.");
                event.preventDefault();
                return;
            }

            console.log("Validation passed! Submitting form..."); // Debugging message
        });
    } else {
        console.error("Error: No se encontró el formulario de perfil.");
    }
});

