"""
Profile management forms.
"""

from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Regexp,
    ValidationError,
)

from authentication.models.user import User


class UpdateProfileForm(FlaskForm):
    """
    Update user profile information.
    """

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=100,
            ),
        ],
        render_kw={
            "placeholder": "John Doe",
        },
    )

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=30,
            ),
            Regexp(
                r"^[A-Za-z0-9_]+$",
                message=(
                    "Username may contain only "
                    "letters, numbers and underscores."
                ),
            ),
        ],
        render_kw={
            "placeholder": "john_doe",
        },
    )

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(),
            Length(
                max=120,
            ),
        ],
        render_kw={
            "placeholder": "john@example.com",
        },
    )

    submit = SubmitField(
        "Save Changes"
    )

    # ------------------------------------------------------
    # Username Validation
    # ------------------------------------------------------

    def validate_username(
        self,
        field,
    ):
        """
        Ensure username remains unique.
        """

        current_user = getattr(
            self,
            "current_user",
            None,
        )

        if (
            current_user
            and field.data == current_user.username
        ):
            return

        existing_user = User.query.filter_by(
            username=field.data
        ).first()

        if existing_user:

            raise ValidationError(
                "Username is already taken."
            )

    # ------------------------------------------------------
    # Email Validation
    # ------------------------------------------------------

    def validate_email(
        self,
        field,
    ):
        """
        Ensure email remains unique.
        """

        current_user = getattr(
            self,
            "current_user",
            None,
        )

        if (
            current_user
            and field.data.lower()
            == current_user.email
        ):
            return

        existing_user = User.query.filter_by(
            email=field.data.lower()
        ).first()

        if existing_user:

            raise ValidationError(
                "Email address is already registered."
            )