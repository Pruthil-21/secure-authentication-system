/*
==========================================================
Secure Authentication System
Main JavaScript
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    initializeApplication();

});


/* ==========================================================
   Application Initialization
========================================================== */

function initializeApplication() {

    initializeTheme();

    initializeThemeToggle();

    initializeFlashMessages();

}


/* ==========================================================
   Theme Initialization
========================================================== */

function initializeTheme() {

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {

        document.body.classList.add("dark-theme");

    }

    updateThemeIcon();

}


/* ==========================================================
   Theme Toggle
========================================================== */

function initializeThemeToggle() {

    const button = document.getElementById("theme-toggle");

    if (!button) return;

    button.addEventListener("click", toggleTheme);

}


/* ==========================================================
   Toggle Theme
========================================================== */

function toggleTheme() {

    document.body.classList.toggle("dark-theme");

    const isDarkTheme = document.body.classList.contains("dark-theme");

    localStorage.setItem(
        "theme",
        isDarkTheme ? "dark" : "light"
    );

    updateThemeIcon();

}


/* ==========================================================
   Update Theme Icon
========================================================== */

function updateThemeIcon() {

    const icon = document.querySelector("#theme-toggle i");

    if (!icon) return;

    if (document.body.classList.contains("dark-theme")) {

        icon.classList.remove("fa-moon");
        icon.classList.add("fa-sun");

    }

    else {

        icon.classList.remove("fa-sun");
        icon.classList.add("fa-moon");

    }

}


/* ==========================================================
   Flash Messages
========================================================== */

function initializeFlashMessages() {

    const flashMessages = document.querySelectorAll(

        ".flash-message"

    );

    flashMessages.forEach(message => {

        const closeButton = message.querySelector(

            ".flash-close"

        );

        if (closeButton) {

            closeButton.addEventListener(

                "click",

                () => {

                    hideFlashMessage(message);

                }

            );

        }

        setTimeout(() => {

            hideFlashMessage(message);

        }, 5000);

    });

}


function hideFlashMessage(message) {

    if (

        !message ||

        message.classList.contains("flash-hide")

    ) {

        return;

    }

    message.classList.add(

        "flash-hide"

    );

    message.addEventListener(

        "animationend",

        () => {

            message.remove();

        },

        {

            once: true

        }

    );

}