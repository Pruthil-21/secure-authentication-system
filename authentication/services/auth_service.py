"""
Authentication service.
"""

from datetime import (
    datetime,
    timedelta,
)

from authentication.extensions import (
    bcrypt,
    db,
)
from authentication.models import User
from authentication.validators.password_validator import (
    validate_password,
)
from authentication.services.login_history_service import (
    LoginHistoryService,
)


class AuthService:
    """
    Handles authentication business logic.
    """

    # ==========================================================
    # Register User
    # ==========================================================

    @staticmethod
    def register_user(form):
        """
        Register a new user.
        """

        email = form.email.data.strip().lower()
        username = form.username.data.strip()

        # Check existing email
        if User.query.filter_by(email=email).first():

            return (
                False,
                "An account with this email already exists.",
            )

        # Check existing username
        if User.query.filter_by(username=username).first():

            return (
                False,
                "Username is already taken.",
            )

        # Validate password
        password_result = validate_password(
            form.password.data
        )

        if not password_result.valid:

            return (
                False,
                password_result.errors[0],
            )

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

        return (
            True,
            "Account created successfully.",
        )

    # ==========================================================
    # Login User
    # ==========================================================

    @staticmethod
    def login_user(
        form,
        request,
    ):
        """
        Authenticate user.
        """

        identifier = form.email_or_username.data.strip()
        password = form.password.data

        ip_address = request.remote_addr

        # Find user
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

        # ------------------------------------------------------
        # Account Lock Check
        # ------------------------------------------------------

        if (
            user.account_locked_until
            and user.account_locked_until > datetime.utcnow()
        ):

            remaining = (
                int(
                    (
                        user.account_locked_until
                        - datetime.utcnow()
                    ).total_seconds()
                    / 60
                )
                + 1
            )

            return (
                False,
                f"Account locked. Try again in {remaining} minute(s).",
                None,
            )

        # ------------------------------------------------------
        # Verify Password
        # ------------------------------------------------------

        if not bcrypt.check_password_hash(
            user.password_hash,
            password,
        ):

            LoginHistoryService.record_login(
                user,
                request,
                successful=False,
            )

            user.failed_login_attempts += 1

            if user.failed_login_attempts >= 5:

                user.account_locked_until = (
                    datetime.utcnow()
                    + timedelta(minutes=15)
                )

            db.session.commit()

            remaining_attempts = max(
                0,
                5 - user.failed_login_attempts,
            )

            if remaining_attempts == 0:

                return (
                    False,
                    "Account locked for 15 minutes due to multiple failed login attempts.",
                    None,
                )

            return (
                False,
                f"Invalid email/username or password. {remaining_attempts} attempt(s) remaining.",
                None,
            )

        # ------------------------------------------------------
        # Successful Login
        # ------------------------------------------------------

        user.failed_login_attempts = 0

        user.account_locked_until = None

        user.login_count += 1

        user.last_login = datetime.utcnow()

        user.last_login_ip = ip_address

        LoginHistoryService.record_login(
            user,
            request,
            successful=True,
        )

        db.session.commit()

        return (
            True,
            "Login successful.",
            user,
        )