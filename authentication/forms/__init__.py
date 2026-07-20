"""
Flask-WTF forms.
"""

from .registration_form import RegistrationForm
from .login_form import LoginForm
from .forgot_password_form import ForgotPasswordForm
from .reset_password_form import ResetPasswordForm
from .resend_verification_form import ResendVerificationForm

__all__ = [
    "RegistrationForm",
    "LoginForm",
    "ForgotPasswordForm",
    "ResetPasswordForm",
    "ResendVerificationForm",
]