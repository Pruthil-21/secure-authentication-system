"""
Email service.

Handles sending emails for:
- Email verification
- Password reset
"""

from flask import (
    current_app,
    render_template,
)

from flask_mail import Message

from authentication.extensions import mail


class EmailService:
    """
    Email service.
    """

    @staticmethod
    def send_email(
        subject,
        recipients,
        html_body,
        text_body=None,
    ):
        """
        Send an email.
        """

        message = Message(
            subject=subject,
            recipients=recipients,
            sender=current_app.config["MAIL_DEFAULT_SENDER"],
        )

        message.html = html_body

        if text_body:

            message.body = text_body

        mail.send(message)

    # ==================================================
    # Email Verification
    # ==================================================

    @staticmethod
    def send_verification_email(
        user,
        verification_url,
    ):
        """
        Send account verification email.
        """

        html_body = render_template(
            "email/verify_email.html",
            user=user,
            verification_url=verification_url,
        )

        text_body = (
            "Verify your email address:\n\n"
            f"{verification_url}"
        )

        EmailService.send_email(
            subject="Verify Your Email Address",
            recipients=[user.email],
            html_body=html_body,
            text_body=text_body,
        )

    # ==================================================
    # Password Reset
    # ==================================================

    @staticmethod
    def send_password_reset_email(
        user,
        reset_url,
    ):
        """
        Send password reset email.
        """

        html_body = render_template(
            "email/reset_password.html",
            user=user,
            reset_url=reset_url,
        )

        text_body = (
            "Reset your password:\n\n"
            f"{reset_url}"
        )

        EmailService.send_email(
            subject="Reset Your Password",
            recipients=[user.email],
            html_body=html_body,
            text_body=text_body,
        )