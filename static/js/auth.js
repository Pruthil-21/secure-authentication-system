/*
==========================================================
Secure Authentication System
Authentication JavaScript
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    initializeAuthentication();

});


/* ==========================================================
   Initialize
========================================================== */

function initializeAuthentication() {

    initializeRegistration();

    initializePasswordVisibility();

    initializePreventDoubleSubmit();

}


/* ==========================================================
   Registration
========================================================== */

function initializeRegistration() {

    const form = document.getElementById("registration-form");

    let usernameTimeout;

    let emailTimeout;

    let usernameAvailable = false;

    let emailAvailable = false;

    if (!form) {

        return;

    }

    const fullName = document.getElementById("full_name");

    const username = document.getElementById("username");

    const email = document.getElementById("email");

    const password = document.getElementById("password");

    const confirmPassword =
        document.getElementById("confirm_password");

    const terms =
        document.getElementById("accept-terms");

    const submitButton =
        document.getElementById("register-button");

    const strengthLabel =
        document.getElementById("password-strength");

    const strengthFill =
        document.getElementById("password-progress-fill");

    const fullNameValidation =
        document.getElementById("fullname-validation");

    const usernameValidation =
        document.getElementById("username-validation");

    const emailValidation =
        document.getElementById("email-validation");

    const confirmValidation =
        document.getElementById("confirm-password-status");

    /* -----------------------------------------
       Field State
    ----------------------------------------- */

    const touched = {

        fullName: false,

        username: false,

        email: false,

        password: false,

        confirmPassword: false

    };


    /* -----------------------------------------
       Full Name
    ----------------------------------------- */

    fullName.addEventListener("input", () => {

        touched.fullName = true;

        updateFullNameValidation();

        updateSubmitButton();

    });


    /* -----------------------------------------
       Username
    ----------------------------------------- */

    username.addEventListener("input", () => {

        touched.username = true;

        updateUsernameValidation();

        clearTimeout(usernameTimeout);

        usernameTimeout = setTimeout(() => {

            checkUsernameAvailability();

        }, 500);

        updateSubmitButton();

    });


    /* -----------------------------------------
       Email
    ----------------------------------------- */

    email.addEventListener("input", () => {

        touched.email = true;

        updateEmailValidation();

        clearTimeout(emailTimeout);

        emailTimeout = setTimeout(() => {

            checkEmailAvailability();

        }, 500);

        updateSubmitButton();

    });


    /* -----------------------------------------
       Password
    ----------------------------------------- */

    password.addEventListener("input", () => {

        touched.password = true;

        updatePasswordStrength();

        updatePasswordChecklist();

        updatePasswordMatch();

        updateSubmitButton();

    });


    /* -----------------------------------------
       Confirm Password
    ----------------------------------------- */

    confirmPassword.addEventListener("input", () => {

        touched.confirmPassword = true;

        updatePasswordMatch();

        updateSubmitButton();

    });


    /* -----------------------------------------
       Terms
    ----------------------------------------- */

    terms.addEventListener("change", () => {

        updateSubmitButton();

    });

    /* -----------------------------------------
       Password Strength
    ----------------------------------------- */

    function updatePasswordStrength() {

        if (!touched.password) {

            strengthLabel.textContent = "";

            strengthFill.style.width = "0%";

            return;

        }

        const score = Validation.calculatePasswordStrength(

            password.value

        );

        const strength = Validation.getPasswordStrength(

            score

        );

        strengthLabel.textContent = strength.label;

        strengthLabel.style.color = strength.color;

        strengthFill.style.width = score + "%";

        const progressText = document.getElementById(
            "password-progress-text"
        );

        if (progressText) {

            progressText.textContent =

                Validation.getPasswordProgressText(

                    password.value

                );

        }

        strengthFill.style.background = strength.color;

    }
    /* -----------------------------------------
   Password Checklist
----------------------------------------- */

    function updatePasswordChecklist() {

    if (!touched.password) {

        return;

    }

    const checks = Validation.getPasswordChecklist(
        password.value
    );

    updateChecklistItem(
        "check-length",
        checks.length
    );

    updateChecklistItem(
        "check-uppercase",
        checks.uppercase
    );

    updateChecklistItem(
        "check-lowercase",
        checks.lowercase
    );

    updateChecklistItem(
        "check-number",
        checks.number
    );

    updateChecklistItem(
        "check-special",
        checks.special
    );

    const warnings =
        document.getElementById(
            "password-warnings"
        );

    warnings.innerHTML = "";

    if (!checks.repeated) {

        warnings.innerHTML +=

        `
        <div class="password-warning">
            <i class="fa-solid fa-triangle-exclamation"></i>
            Repeated characters detected
        </div>
        `;

    }

    if (!checks.sequence) {

        warnings.innerHTML +=

        `
        <div class="password-warning">
            <i class="fa-solid fa-triangle-exclamation"></i>
            Sequential numbers detected
        </div>
        `;

    }

    if (!checks.commonWord) {

        warnings.innerHTML +=

        `
        <div class="password-warning">
            <i class="fa-solid fa-triangle-exclamation"></i>
            Common password detected
        </div>
        `;

    }

}


    /* -----------------------------------------
       Checklist Item
    ----------------------------------------- */

    function updateChecklistItem(id, valid) {

        const item = document.getElementById(id);

        if (!item) return;

        const icon = item.querySelector("i");

        if (valid) {

            icon.className =
                "fa-solid fa-circle-check";

            item.style.color = "#16A34A";

        }

        else {

            icon.className =
                "fa-solid fa-circle-xmark";

            item.style.color = "#DC2626";

        }

    }


    /* -----------------------------------------
       Full Name Validation
    ----------------------------------------- */

    function updateFullNameValidation() {

        if (!touched.fullName) {

            return;

        }

        const valid = Validation.isValidFullName(

            fullName.value

        );

        Validation.setValidationMessage(

            fullNameValidation,

            valid
                ? "✓ Valid full name"
                : "Minimum 3 characters required",

            valid

        );

        setInputState(

            fullName,

            valid

        );

    }

    /* -----------------------------------------
       Username Validation
    ----------------------------------------- */

    function updateUsernameValidation() {

        if (!touched.username) {

            return;

        }

        const valid = Validation.isValidUsername(

            username.value

        );

        Validation.setValidationMessage(

            usernameValidation,

            valid
                ? "✓ Username format looks good"
                : "Only letters, numbers and underscores",

            valid

        );

        setInputState(

            username,

            valid

        );

    }

    /* -----------------------------------------
       Email Validation
    ----------------------------------------- */

    function updateEmailValidation() {

        if (!touched.email) {

            return;

        }

        const valid = Validation.isValidEmail(

            email.value

        );

        Validation.setValidationMessage(

            emailValidation,

            valid
                ? "✓ Valid email address"
                : "Please enter a valid email address",

            valid

        );

        setInputState(

            email,

            valid

        );

    }


/* -----------------------------------------
   Password Match
----------------------------------------- */

function updatePasswordMatch() {

    if (!touched.confirmPassword) {

        return;

    }

    const state = Validation.getPasswordMatchState(

        password.value,

        confirmPassword.value

    );

    Validation.setValidationMessage(

        confirmValidation,

        state.message,

        state.valid

    );

    setInputState(

        confirmPassword,

        state.valid

    );

}


/* -----------------------------------------
   Username Availability
----------------------------------------- */

async function checkUsernameAvailability() {

    if (!Validation.isValidUsername(username.value)) {

        usernameAvailable = false;

        return;

    }

    try {

        const response = await fetch(

            `/check-username?username=${encodeURIComponent(username.value)}`

        );

        const data = await response.json();

        usernameAvailable = data.available;

        if (data.available) {

            usernameValidation.innerHTML =

                "✓ Username is available.";

            usernameValidation.className =

                "validation-message success";

        }

        else {

            usernameValidation.innerHTML =

                `✖ Username already exists.
                <a href="/login" class="validation-link">
                    Login instead →
                </a>`;

            usernameValidation.className =

                "validation-message error";

        }

        setInputState(

            username,

            data.available

        );

        updateSubmitButton();

    }

    catch (error) {

        console.error(

            "Username check failed:",

            error

        );

    }

}


/* -----------------------------------------
   Email Availability
----------------------------------------- */

async function checkEmailAvailability() {

    if (!Validation.isValidEmail(email.value)) {

        emailAvailable = false;

        return;

    }

    try {

        const response = await fetch(

            `/check-email?email=${encodeURIComponent(email.value)}`

        );

        const data = await response.json();

        emailAvailable = data.available;

        if (data.available) {

            emailValidation.innerHTML =

                "✓ Email is available.";

            emailValidation.className =

                "validation-message success";

        }

        else {

            emailValidation.innerHTML =

                `✖ An account with this email already exists.
                <a href="/login" class="validation-link">
                    Login instead →
                </a>`;

            emailValidation.className =

                "validation-message error";

        }

        setInputState(

            email,

            data.available

        );

        updateSubmitButton();

    }

    catch (error) {

        console.error(

            "Email check failed:",

            error

        );

    }

}
    /* -----------------------------------------
   Submit Button
----------------------------------------- */

    function updateSubmitButton() {

        const formValid = Validation.isRegistrationFormValid({

            fullName: fullName.value,

            username: username.value,

            email: email.value,

            password: password.value,

            confirmPassword: confirmPassword.value

        });

        submitButton.disabled = !(

            formValid &&

            usernameAvailable &&

            emailAvailable &&

            terms.checked

        );
        submitButton.style.opacity =

            submitButton.disabled

                ? ".65"

                : "1";

    }


    /* -----------------------------------------
       Initial Validation
    ----------------------------------------- */

    updateSubmitButton();

}


/* ==========================================================
   Password Visibility
========================================================== */

function initializePasswordVisibility() {

    document

        .querySelectorAll(".password-toggle")

        .forEach(button => {

            button.addEventListener("click", () => {

                const input = document.getElementById(

                    button.dataset.target

                );

                if (!input) return;

                const icon = button.querySelector("i");

                if (input.type === "password") {

                    input.type = "text";

                    icon.className =

                        "fa-solid fa-eye-slash";

                }

                else {

                    input.type = "password";

                    icon.className =

                        "fa-solid fa-eye";

                }

            });

        });

}
/* ==========================================================
   Prevent Double Submission
========================================================== */

function initializePreventDoubleSubmit() {

    document.querySelectorAll("form").forEach(form => {

        form.addEventListener("submit", event => {

            const submitButton = form.querySelector(

                "#register-button, button[type='submit'], input[type='submit']"

            );

            if (!submitButton) {

                return;

            }

            // Prevent accidental submission if somehow triggered
            if (submitButton.disabled) {

                event.preventDefault();

                return;

            }

            submitButton.disabled = true;

            if (submitButton.tagName === "BUTTON") {

                submitButton.dataset.originalText =
                    submitButton.innerHTML;

                submitButton.innerHTML =

                    '<i class="fa-solid fa-spinner fa-spin"></i> Creating Account...';

            }

            else {

                submitButton.value =

                    "Creating Account...";

            }

        });

    });

}


/* ==========================================================
   Utility
========================================================== */

function setInputState(input, valid) {

    if (!input) return;

    input.classList.remove(

        "valid",

        "invalid"

    );

    if (input.value.trim().length === 0) {

        return;

    }

    input.classList.add(

        valid

            ? "valid"

            : "invalid"

    );

}