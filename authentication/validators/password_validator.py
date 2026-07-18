"""
Password validation utilities.
"""

import math
import re


SPECIAL_CHARACTERS = r"!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?"


class PasswordValidationResult:
    """
    Stores the result of password validation.
    """

    def __init__(
        self,
        valid: bool,
        score: int,
        strength: str,
        errors: list[str],
    ):
        self.valid = valid
        self.score = score
        self.strength = strength
        self.errors = errors


def calculate_entropy(password: str) -> float:
    """
    Estimate password entropy.
    """

    pool = 0

    if re.search(r"[a-z]", password):
        pool += 26

    if re.search(r"[A-Z]", password):
        pool += 26

    if re.search(r"\d", password):
        pool += 10

    if re.search(rf"[{re.escape(SPECIAL_CHARACTERS)}]", password):
        pool += len(SPECIAL_CHARACTERS)

    if pool == 0:
        return 0

    return len(password) * math.log2(pool)


def validate_password(password: str) -> PasswordValidationResult:
    """
    Validate password strength.
    """

    errors = []

    score = 0

    if len(password) < 12:
        errors.append("Password must contain at least 12 characters.")
    else:
        score += 20

    if re.search(r"[A-Z]", password):
        score += 15
    else:
        errors.append("Include at least one uppercase letter.")

    if re.search(r"[a-z]", password):
        score += 15
    else:
        errors.append("Include at least one lowercase letter.")

    if re.search(r"\d", password):
        score += 15
    else:
        errors.append("Include at least one number.")

    if re.search(rf"[{re.escape(SPECIAL_CHARACTERS)}]", password):
        score += 15
    else:
        errors.append("Include at least one special character.")

    if re.search(r"(.)\1{2,}", password):
        errors.append("Avoid repeated characters.")
    else:
        score += 10

    sequences = [
        "123456",
        "abcdef",
        "qwerty",
        "password",
    ]

    if any(seq in password.lower() for seq in sequences):
        errors.append("Avoid predictable sequences.")
    else:
        score += 10

    entropy = calculate_entropy(password)

    if entropy >= 60:
        score += 15

    score = min(score, 100)

    if score >= 90:
        strength = "Very Strong"
    elif score >= 75:
        strength = "Strong"
    elif score >= 60:
        strength = "Moderate"
    elif score >= 40:
        strength = "Weak"
    else:
        strength = "Very Weak"

    return PasswordValidationResult(
        valid=len(errors) == 0,
        score=score,
        strength=strength,
        errors=errors,
    )