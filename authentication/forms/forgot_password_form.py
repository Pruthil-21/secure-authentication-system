"""
Forgot password form.
"""

from flask_wtf import FlaskForm

from wtforms import (
    EmailField,
    SubmitField,
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
)


class ForgotPasswordForm(FlaskForm):
    """
    Form used to request a password reset email.
    """

    email = EmailField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(),
            Length(max=120),
        ],
        render_kw={
            "placeholder": "Enter your email address",
            "autocomplete": "email",
        },
    )

    submit = SubmitField(
        "Send Reset Link"
    )