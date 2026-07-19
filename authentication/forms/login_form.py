"""
Login form.
"""

from flask_wtf import FlaskForm

from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
)

from wtforms.validators import (
    DataRequired,
    Length,
)


class LoginForm(FlaskForm):
    """
    User login form.
    """

    email_or_username = StringField(
        "Email or Username",
        validators=[
            DataRequired(
                message="Email or Username is required."
            ),
            Length(
                min=3,
                max=120,
            ),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(
                message="Password is required."
            ),
        ],
    )

    remember = BooleanField(
        "Remember Me"
    )

    submit = SubmitField(
        "Login"
    )