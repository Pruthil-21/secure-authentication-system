"""
Profile management service.
"""

from authentication.extensions import db

from authentication.models.user import User


class ProfileService:
    """
    Service for profile-related operations.
    """

    @staticmethod
    def get_profile_data(user):
        """
        Return profile information for the authenticated user.
        """

        return {
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at,
            "last_login": user.last_login,
            "login_count": user.login_count,
            "failed_login_attempts": user.failed_login_attempts,
            "last_login_ip": user.last_login_ip,
            "email_verified": user.is_email_verified,
            "two_factor_enabled": user.two_factor_enabled,
        }

    @staticmethod
    def populate_form(form, user):
        """
        Populate the profile form with the current user's data.
        """

        form.full_name.data = user.full_name
        form.username.data = user.username
        form.email.data = user.email

    @staticmethod
    def update_profile(user, form):
        """
        Update the user's profile information.
        """

        changes = []

        full_name = form.full_name.data.strip()

        username = form.username.data.strip()

        email = form.email.data.strip().lower()

        if user.full_name != full_name:

            user.full_name = full_name

            changes.append("Full Name")

        if user.username != username:

            user.username = username

            changes.append("Username")

        if user.email != email:

            user.email = email

            user.is_email_verified = False

            changes.append("Email Address")

        db.session.commit()

        return changes