"""
Flask-WTF forms.
"""

from .registration_form import RegistrationForm
from .login_form import LoginForm
from .forgot_password_form import ForgotPasswordForm
from .reset_password_form import ResetPasswordForm
from .resend_verification_form import ResendVerificationForm
from .enable_two_factor_form import EnableTwoFactorForm
from .disable_two_factor_form import DisableTwoFactorForm
from .verify_two_factor_form import VerifyTwoFactorForm
from .change_password_form import ChangePasswordForm

__all__ = [
    "RegistrationForm",
    "LoginForm",
    "ForgotPasswordForm",
    "ResetPasswordForm",
    "ResendVerificationForm",
    "EnableTwoFactorForm",
    "DisableTwoFactorForm",
    "VerifyTwoFactorForm",
    "ChangePasswordForm",
]