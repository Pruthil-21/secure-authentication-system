"""
Token service.

Handles secure token generation and verification for:
- Email verification
- Password reset
"""

from itsdangerous import (
    URLSafeTimedSerializer,
    BadSignature,
    SignatureExpired,
)

from flask import current_app


class TokenService:
    """
    Generate and verify signed tokens.
    """

    @staticmethod
    def _serializer():
        """
        Return configured serializer.
        """

        return URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"]
        )

    # --------------------------------------------------
    # Email Verification
    # --------------------------------------------------

    @staticmethod
    def generate_email_token(email):
        """
        Generate an email verification token.
        """

        serializer = TokenService._serializer()

        return serializer.dumps(
            email,
            salt="email-verification",
        )

    @staticmethod
    def verify_email_token(
        token,
        max_age=1800,
    ):
        """
        Verify an email verification token.

        Returns:
            email or None
        """

        serializer = TokenService._serializer()

        try:

            return serializer.loads(
                token,
                salt="email-verification",
                max_age=max_age,
            )

        except (
            SignatureExpired,
            BadSignature,
        ):

            return None

    # --------------------------------------------------
    # Password Reset
    # --------------------------------------------------

    @staticmethod
    def generate_reset_token(email):
        """
        Generate a password reset token.
        """

        serializer = TokenService._serializer()

        return serializer.dumps(
            email,
            salt="password-reset",
        )

    @staticmethod
    def verify_reset_token(
        token,
        max_age=1800,
    ):
        """
        Verify a password reset token.

        Returns:
            email or None
        """

        serializer = TokenService._serializer()

        try:

            return serializer.loads(
                token,
                salt="password-reset",
                max_age=max_age,
            )

        except (
            SignatureExpired,
            BadSignature,
        ):

            return None