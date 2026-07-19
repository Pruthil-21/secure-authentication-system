"use strict";

/* ==========================================================
   Reset Password Page
========================================================== */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const password =
            document.getElementById("password");

        const confirmPassword =
            document.getElementById("confirm_password");

        if (!password || !confirmPassword) {

            return;

        }

        const strengthFill =
            document.getElementById("strength-fill");

        const strengthText =
            document.getElementById("strength-text");

        const passwordMatch =
            document.getElementById("password-match");

        const checklist =
            document.getElementById("password-checklist");

        const form =
            document.querySelector("form");

        const submitButton =
            form.querySelector(
                'input[type="submit"], button[type="submit"]'
            );

        /* ==============================================
           Update Password Strength
        ============================================== */

        function updatePasswordStrength() {

            const value = password.value;

            const score =
                Validation.calculatePasswordStrength(
                    value
                );

            const strength =
                Validation.getPasswordStrength(
                    score
                );

            strengthFill.style.width =
                `${score}%`;

            strengthFill.style.backgroundColor =
                strength.color;

            strengthText.textContent =
                `${strength.label} (${score}%)`;

        }

        /* ==============================================
           Update Checklist
        ============================================== */

        function updateChecklist() {

            const checks =
                Validation.getPasswordChecklist(
                    password.value
                );

            checklist
                .querySelectorAll("li")
                .forEach(item => {

                    const rule =
                        item.dataset.rule;

                    const passed =
                        checks[rule];

                    item.classList.toggle(
                        "valid",
                        passed
                    );

                    item.classList.toggle(
                        "invalid",
                        !passed
                    );

                    item.innerHTML = passed

                        ? `✅ ${item.textContent.replace(/^❌|^✅/, "").trim()}`

                        : `❌ ${item.textContent.replace(/^❌|^✅/, "").trim()}`;

                });

        }

        /* ==============================================
           Password Match
        ============================================== */

        function updatePasswordMatch() {

            const state =
                Validation.getPasswordMatchState(

                    password.value,

                    confirmPassword.value

                );

            Validation.setValidationMessage(

                passwordMatch,

                state.message,

                state.valid

            );

        }

        /* ==============================================
           Enable Submit Button
        ============================================== */

        function updateSubmitState() {

            const valid =

                Validation.isFormPasswordValid(
                    password.value
                ) &&

                Validation.passwordsMatch(
                    password.value,
                    confirmPassword.value
                );

            submitButton.disabled = !valid;

        }

        /* ==============================================
           Refresh UI
        ============================================== */

        function refresh() {

            updatePasswordStrength();

            updateChecklist();

            updatePasswordMatch();

            updateSubmitState();

        }

        password.addEventListener(
            "input",
            refresh,
        );

        confirmPassword.addEventListener(
            "input",
            refresh,
        );

        refresh();

        /* ==============================================
           Prevent Double Submit
        ============================================== */

        form.addEventListener(
            "submit",
            () => {

                submitButton.disabled = true;

                if (

                    submitButton.tagName
                        .toLowerCase() === "input"

                ) {

                    submitButton.value =
                        "Resetting Password...";

                }

                else {

                    submitButton.innerHTML = `
                        <i class="fa-solid fa-spinner fa-spin"></i>
                        Resetting Password...
                    `;

                }

            }
        );

    }
);

/* ==========================================================
   Password Visibility Toggle
========================================================== */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        document
            .querySelectorAll(".password-toggle")
            .forEach(button => {

                button.addEventListener(
                    "click",
                    () => {

                        const input =
                            document.getElementById(
                                button.dataset.target
                            );

                        const icon =
                            button.querySelector("i");

                        if (!input) {

                            return;

                        }

                        if (
                            input.type === "password"
                        ) {

                            input.type = "text";

                            icon.classList.remove(
                                "fa-eye"
                            );

                            icon.classList.add(
                                "fa-eye-slash"
                            );

                        }

                        else {

                            input.type = "password";

                            icon.classList.remove(
                                "fa-eye-slash"
                            );

                            icon.classList.add(
                                "fa-eye"
                            );

                        }

                    }
                );

            });

    }
);