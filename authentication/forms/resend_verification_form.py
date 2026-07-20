"""
Resend verification email form.
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


class ResendVerificationForm(FlaskForm):
    """
    Form used to resend the verification email.
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
        "Resend Verification Email"
    )