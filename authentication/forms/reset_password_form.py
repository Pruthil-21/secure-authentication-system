"""
Reset password form.
"""

from flask_wtf import FlaskForm

from wtforms import (
    PasswordField,
    SubmitField,
)

from wtforms.validators import (
    DataRequired,
    EqualTo,
    Length,
    ValidationError,
)

from authentication.validators.password_validator import (
    validate_password,
)


class ResetPasswordForm(FlaskForm):
    """
    Form used to reset a user's password.
    """

    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(
                min=12,
                max=128,
            ),
        ],
        render_kw={
            "autocomplete": "new-password",
            "placeholder": "Enter your new password",
        },
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match.",
            ),
        ],
        render_kw={
            "autocomplete": "new-password",
            "placeholder": "Confirm your new password",
        },
    )

    submit = SubmitField(
        "Reset Password"
    )

    # --------------------------------------------------
    # Password Validation
    # --------------------------------------------------

    def validate_password(
        self,
        field,
    ):
        """
        Validate password strength.
        """

        result = validate_password(
            field.data,
        )

        if not result.valid:

            raise ValidationError(
                result.errors[0]
            )