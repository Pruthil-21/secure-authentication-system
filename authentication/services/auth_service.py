"""
Authentication service.
"""

from authentication.extensions import bcrypt, db
from authentication.models import User
from authentication.validators.password_validator import validate_password


class AuthService:
    """
    Handles authentication business logic.
    """

    @staticmethod
    def register_user(form):
        """
        Register a new user.
        """

        email = form.email.data.strip().lower()
        username = form.username.data.strip()

        # Check existing email
        if User.query.filter_by(email=email).first():
            return False, "An account with this email already exists."

        # Check existing username
        if User.query.filter_by(username=username).first():
            return False, "Username is already taken."

        # Validate password
        password_result = validate_password(form.password.data)

        if not password_result.valid:
            return False, password_result.errors[0]

        # Hash password
        password_hash = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        # Create user
        user = User(
            full_name=form.full_name.data.strip(),
            username=username,
            email=email,
            password_hash=password_hash,
        )

        db.session.add(user)
        db.session.commit()

        return True, "Account created successfully."

    @staticmethod
    def login_user(form):
        """
        Authenticate a user using email or username.
        """

        identifier = form.email_or_username.data.strip()
        password = form.password.data

        # Find user by email or username
        user = User.query.filter(
            (User.email == identifier.lower())
            | (User.username == identifier)
        ).first()

        if user is None:
            return (
                False,
                "Invalid email/username or password.",
                None,
            )

        # Verify password
        if not bcrypt.check_password_hash(
            user.password_hash,
            password,
        ):
            return (
                False,
                "Invalid email/username or password.",
                None,
            )

        return (
            True,
            "Login successful.",
            user,
        )