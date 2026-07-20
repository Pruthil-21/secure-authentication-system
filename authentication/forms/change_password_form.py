"""
Change Password form.
"""

from flask_wtf import FlaskForm

from wtforms import (
    PasswordField,
    SubmitField,
)

from wtforms.validators import (
    DataRequired,
    EqualTo,
)

from authentication.validators.password_validator import (
    validate_password,
)


class ChangePasswordForm(FlaskForm):
    """
    Change account password.
    """

    current_password = PasswordField(
        "Current Password",
        validators=[
            DataRequired(),
        ],
    )

    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
        ],
    )

    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo(
                "new_password",
                message="Passwords must match.",
            ),
        ],
    )

    submit = SubmitField(
        "Change Password",
    )

    def validate(self, extra_validators=None):

        if not super().validate(
            extra_validators=extra_validators,
        ):
            return False

        result = validate_password(
            self.new_password.data,
        )

        if not result.valid:

            self.new_password.errors.append(
                result.errors[0],
            )

            return False

        return True