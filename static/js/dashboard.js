/*
==========================================================
Secure Authentication System
Dashboard JavaScript
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    const progress = document.getElementById(
        "security-progress"
    );

    if (!progress) return;

    const score = progress.dataset.score;

    progress.style.width = `${score}%`;

});

/* ==========================================================
   Dashboard Initialization
========================================================== */

function initializeDashboard() {

    console.log(
        "Dashboard initialized."
    );

}