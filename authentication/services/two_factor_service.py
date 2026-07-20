"""
Two-Factor Authentication service.
"""

import pyotp

from authentication.extensions import (
    bcrypt,
    db,
)


class TwoFactorService:
    """
    Handles TOTP generation and verification.
    """

    @staticmethod
    def generate_secret():
        """
        Generate a new TOTP secret.
        """

        return pyotp.random_base32()

    @staticmethod
    def generate_uri(user):
        """
        Generate the provisioning URI for
        Google Authenticator.
        """

        totp = pyotp.TOTP(
            user.two_factor_secret,
        )

        return totp.provisioning_uri(

            name=user.email,

            issuer_name="Secure Authentication System",

        )

    @staticmethod
    def verify_code(
        secret,
        code,
    ):
        """
        Verify a TOTP code.
        """

        totp = pyotp.TOTP(
            secret,
        )

        return totp.verify(
            code,
        )
        
    @staticmethod
    def disable_two_factor(
        user,
        password,
        otp_code,
    ):
        """
        Disable Two-Factor Authentication.
        """

        if not bcrypt.check_password_hash(
            user.password_hash,
            password,
        ):

            return (
                False,
                "Incorrect password.",
            )

        if not user.two_factor_secret:

            return (
                False,
                "Two-Factor Authentication is not configured.",
            )

        if not TwoFactorService.verify_code(
            user.two_factor_secret,
            otp_code,
        ):

            return (
                False,
                "Invalid authentication code.",
            )

        user.two_factor_enabled = False

        user.two_factor_secret = None

        db.session.commit()

        return (
            True,
            "Two-Factor Authentication has been disabled.",
        )