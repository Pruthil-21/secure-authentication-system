"use strict";

/* ==========================================================
   Profile Page
========================================================== */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form = document.querySelector("form");

        if (!form) {

            return;

        }

        const fullName = document.getElementById(
            "full_name"
        );

        const username = document.getElementById(
            "username"
        );

        const email = document.getElementById(
            "email"
        );

        const submitButton = form.querySelector(
            'input[type="submit"], button[type="submit"]'
        );

        const initialValues = {

            fullName: fullName.value,

            username: username.value,

            email: email.value,

        };

        let hasChanges = false;

        /* ==============================================
           Detect Changes
        ============================================== */

        function detectChanges() {

            hasChanges = (

                fullName.value !== initialValues.fullName ||

                username.value !== initialValues.username ||

                email.value !== initialValues.email

            );

            submitButton.disabled = !hasChanges;

        }

        fullName.addEventListener(
            "input",
            detectChanges,
        );

        username.addEventListener(
            "input",
            detectChanges,
        );

        email.addEventListener(
            "input",
            detectChanges,
        );

        detectChanges();

        /* ==============================================
           Warn Before Leaving
        ============================================== */

        window.addEventListener(
            "beforeunload",
            function (event) {

                if (!hasChanges) {

                    return;

                }

                event.preventDefault();

                event.returnValue = "";

            }
        );

        /* ==============================================
           Remove Warning After Submit
        ============================================== */

        form.addEventListener(
            "submit",
            () => {

                hasChanges = false;

            }
        );

    }
);