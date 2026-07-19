/*
==========================================================
Secure Authentication System
Validation Utilities
==========================================================
*/


/* ==========================================================
   Common Password Lists
========================================================== */

const COMMON_PASSWORD_WORDS = [

    "password",
    "password123",
    "123456",
    "12345678",
    "123456789",
    "admin",
    "admin123",
    "qwerty",
    "abc123",
    "welcome",
    "letmein",
    "guest",
    "root"

];


/* ==========================================================
   Character Checks
========================================================== */

function hasUppercase(password) {

    return /[A-Z]/.test(password);

}


function hasLowercase(password) {

    return /[a-z]/.test(password);

}


function hasNumber(password) {

    return /\d/.test(password);

}


function hasSpecialCharacter(password) {

    return /[^A-Za-z0-9]/.test(password);

}


function hasMinimumLength(password) {

    return password.length >= 12;

}


/* ==========================================================
   Sequential Characters
========================================================== */

function hasSequentialNumbers(password) {

    const sequences = [

        "0123",
        "1234",
        "2345",
        "3456",
        "4567",
        "5678",
        "6789",
        "9876",
        "8765",
        "7654",
        "6543",
        "5432",
        "4321"

    ];

    const lower = password.toLowerCase();

    return sequences.some(sequence => lower.includes(sequence));

}


/* ==========================================================
   Repeated Characters
========================================================== */

function hasRepeatedCharacters(password) {

    return /(.)\1{2,}/.test(password);

}


/* ==========================================================
   Common Word Detection
========================================================== */

function containsCommonWord(password) {

    const lower = password.toLowerCase();

    return COMMON_PASSWORD_WORDS.some(word =>
        lower.includes(word)
    );

}


/* ==========================================================
   Character Diversity
========================================================== */

function uniqueCharacterRatio(password) {

    if (password.length === 0) {

        return 0;

    }

    const uniqueCharacters = new Set(password);

    return uniqueCharacters.size / password.length;

}


/* ==========================================================
   Password Strength
========================================================== */

function calculatePasswordStrength(password) {

    if (!password) {

        return 0;

    }

    let score = 0;

    // Length

    if (password.length >= 12) score += 20;

    if (password.length >= 16) score += 10;

    // Character Types

    if (hasUppercase(password)) score += 15;

    if (hasLowercase(password)) score += 15;

    if (hasNumber(password)) score += 15;

    if (hasSpecialCharacter(password)) score += 15;

    // Diversity

    const diversity = uniqueCharacterRatio(password);

    if (diversity >= 0.80) {

        score += 10;

    }

    // Penalties

    if (hasSequentialNumbers(password)) {

        score -= 10;

    }

    if (hasRepeatedCharacters(password)) {

        score -= 10;

    }

    if (containsCommonWord(password)) {

        score -= 20;

    }

    // Clamp

    score = Math.max(0, Math.min(score, 100));

    return score;

}


/* ==========================================================
   Password Strength Label
========================================================== */

function getPasswordStrength(score) {

    if (score >= 90) {

        return {

            label: "Very Strong",

            color: "#16A34A"

        };

    }

    if (score >= 70) {

        return {

            label: "Strong",

            color: "#22C55E"

        };

    }

    if (score >= 50) {

        return {

            label: "Moderate",

            color: "#F59E0B"

        };

    }

    if (score >= 30) {

        return {

            label: "Weak",

            color: "#F97316"

        };

    }

    return {

        label: "Very Weak",

        color: "#EF4444"

    };

}
/* ==========================================================
   Password Checklist
========================================================== */

function getPasswordChecklist(password) {

    return {

        length: hasMinimumLength(password),

        uppercase: hasUppercase(password),

        lowercase: hasLowercase(password),

        number: hasNumber(password),

        special: hasSpecialCharacter(password),

        repeated: !hasRepeatedCharacters(password),

        sequence: !hasSequentialNumbers(password),

        commonWord: !containsCommonWord(password)

    };

}


/* ==========================================================
   Password Validation
========================================================== */

function isFormPasswordValid(password) {

    const checks = getPasswordChecklist(password);

    return (

        checks.length &&

        checks.uppercase &&

        checks.lowercase &&

        checks.number &&

        checks.special &&

        checks.repeated &&

        checks.sequence &&

        checks.commonWord

    );

}


/* ==========================================================
   Password Progress
========================================================== */

function getPasswordProgress(password) {

    const checks = getPasswordChecklist(password);

    const total = Object.keys(checks).length;

    const passed = Object.values(checks).filter(Boolean).length;

    return Math.round((passed / total) * 100);

}


/* ==========================================================
   Email Validation
========================================================== */

function isValidEmail(email) {

    if (!email) {

        return false;

    }

    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());

}


/* ==========================================================
   Username Validation
========================================================== */

function isValidUsername(username) {

    if (!username) {

        return false;

    }

    username = username.trim();

    if (username.length < 3 || username.length > 30) {

        return false;

    }

    return /^[A-Za-z0-9_]+$/.test(username);

}


/* ==========================================================
   Full Name Validation
========================================================== */

function isValidFullName(name) {

    if (!name) {

        return false;

    }

    name = name.trim();

    return name.length >= 3;

}


/* ==========================================================
   Password Match
========================================================== */

function passwordsMatch(password, confirmPassword) {

    return (

        confirmPassword.length > 0 &&

        password === confirmPassword

    );

}


/* ==========================================================
   Password Match State
========================================================== */

function getPasswordMatchState(password, confirmPassword) {

    if (confirmPassword.length === 0) {

        return {

            valid: false,

            message: ""

        };

    }

    if (password === confirmPassword) {

        return {

            valid: true,

            message: "Passwords match"

        };

    }

    return {

        valid: false,

        message: "Passwords do not match"

    };

}


/* ==========================================================
   Registration Form Validation
========================================================== */

function isRegistrationFormValid(data) {

    return (

        isValidFullName(data.fullName) &&

        isValidUsername(data.username) &&

        isValidEmail(data.email) &&

        isFormPasswordValid(data.password) &&

        passwordsMatch(

            data.password,

            data.confirmPassword

        )

    );

}
/* ==========================================================
   Strength Color Helper
========================================================== */

function getStrengthColor(score) {

    return getPasswordStrength(score).color;

}


/* ==========================================================
   Field State Helper
========================================================== */

function getFieldState(valid) {

    return {

        borderColor: valid ? "#22C55E" : "#EF4444",

        textColor: valid ? "#16A34A" : "#DC2626"

    };

}


/* ==========================================================
   Validation Message Helper
========================================================== */

function setValidationMessage(

    element,

    message,

    valid,

    allowHtml = false

) {

    if (!element) {

        return;

    }

    if (allowHtml) {

        element.innerHTML = message;

    }

    else {

        element.textContent = message;

    }

    element.style.color = valid

        ? "#16A34A"

        : "#DC2626";

}

/* ==========================================================
   Password Requirement Labels
========================================================== */

function getPasswordRequirementLabels() {

    return {

        length: "At least 12 characters",

        uppercase: "Contains an uppercase letter",

        lowercase: "Contains a lowercase letter",

        number: "Contains a number",

        special: "Contains a special character",

        repeated: "No repeated characters",

        sequence: "No sequential numbers",

        commonWord: "No common/common dictionary words"

    };

}


/* ==========================================================
   Completed Requirement Count
========================================================== */

function getCompletedRequirements(password) {

    const checks = getPasswordChecklist(password);

    return Object.values(checks).filter(Boolean).length;

}


/* ==========================================================
   Total Requirement Count
========================================================== */

function getTotalRequirements() {

    return Object.keys(

        getPasswordChecklist("")

    ).length;

}


/* ==========================================================
   Password Progress Text
========================================================== */

function getPasswordProgressText(password) {

    const checklist = getPasswordChecklist(password);

    let completed = 0;

    // Only count the actual password requirements
    if (checklist.length) completed++;
    if (checklist.uppercase) completed++;
    if (checklist.lowercase) completed++;
    if (checklist.number) completed++;
    if (checklist.special) completed++;

    return `${completed} / 5 Requirements Completed`;

}

/* ==========================================================
   Empty Check
========================================================== */

function isEmpty(value) {

    return value.trim().length === 0;

}


/* ==========================================================
   Trim Helper
========================================================== */

function sanitizeInput(value) {

    return value.trim();

}


/* ==========================================================
   Registration Data Helper
========================================================== */

function getRegistrationData() {

    return {

        fullName:

            sanitizeInput(

                document.getElementById("full_name")?.value || ""

            ),

        username:

            sanitizeInput(

                document.getElementById("username")?.value || ""

            ),

        email:

            sanitizeInput(

                document.getElementById("email")?.value || ""

            ),

        password:

            document.getElementById("password")?.value || "",

        confirmPassword:

            document.getElementById("confirm_password")?.value || ""

    };

}


/* ==========================================================
   Public Validation API
========================================================== */

const Validation = {

    calculatePasswordStrength,

    getPasswordStrength,

    getStrengthColor,

    getPasswordChecklist,

    getPasswordProgress,

    getPasswordProgressText,

    getPasswordRequirementLabels,

    getCompletedRequirements,

    getTotalRequirements,

    isFormPasswordValid,

    isValidEmail,

    isValidUsername,

    isValidFullName,

    passwordsMatch,

    getPasswordMatchState,

    isRegistrationFormValid,

    getRegistrationData,

    setValidationMessage,

    getFieldState,

    sanitizeInput,

    isEmpty

};

window.Validation = Validation;