"use strict";

/* ==========================================================
   Forgot Password Page
========================================================== */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form = document.querySelector("form");

        if (!form) {

            return;

        }

        const submitButton = form.querySelector(
            'input[type="submit"], button[type="submit"]'
        );

        if (!submitButton) {

            return;

        }

        form.addEventListener(
            "submit",
            () => {

                submitButton.disabled = true;

                if (
                    submitButton.tagName.toLowerCase() === "input"
                ) {

                    submitButton.value =
                        "Sending Reset Link...";

                }

                else {

                    submitButton.innerHTML = `
                        <i class="fa-solid fa-spinner fa-spin"></i>
                        Sending Reset Link...
                    `;

                }

            }
        );

    }
);