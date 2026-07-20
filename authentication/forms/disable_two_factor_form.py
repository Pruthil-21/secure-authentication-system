"""
Disable Two-Factor Authentication form.
"""

from flask_wtf import FlaskForm

from wtforms import (
    PasswordField,
    StringField,
    SubmitField,
)

from wtforms.validators import (
    DataRequired,
    Length,
    Regexp,
)


class DisableTwoFactorForm(FlaskForm):
    """
    Disable Two-Factor Authentication.
    """

    password = PasswordField(
        "Current Password",
        validators=[
            DataRequired(),
        ],
    )

    otp_code = StringField(
        "Authentication Code",
        validators=[
            DataRequired(),
            Length(
                min=6,
                max=6,
            ),
            Regexp(
                r"^\d{6}$",
                message="Enter a valid 6-digit code.",
            ),
        ],
    )

    submit = SubmitField(
        "Disable Two-Factor Authentication",
    )