"""
Flask-WTF forms.
"""

from authentication.forms.registration_form import RegistrationForm
from .login_form import LoginForm

__all__ = [
    "RegistrationForm",
]