"""
Verify Two-Factor Authentication form.
"""

from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SubmitField,
)

from wtforms.validators import (
    DataRequired,
    Length,
    Regexp,
)


class VerifyTwoFactorForm(FlaskForm):
    """
    Verify a login using TOTP.
    """

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
        render_kw={
            "placeholder": "Enter the 6-digit code",
            "autocomplete": "one-time-code",
        },
    )

    submit = SubmitField(
        "Verify & Sign In",
    )