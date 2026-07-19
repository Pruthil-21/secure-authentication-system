"""
Dashboard service.
"""

from authentication.models import LoginHistory


class DashboardService:
    """
    Handles dashboard related business logic.
    """

    @staticmethod
    def get_dashboard_data(user):
        """
        Returns all dashboard data required by the template.
        """

        recent_logins = DashboardService.get_recent_logins(user)

        security_score = DashboardService.calculate_security_score(user)

        statistics = DashboardService.get_statistics(user)

        return {

            "recent_logins": recent_logins,

            "security_score": security_score,

            "statistics": statistics,

        }

    @staticmethod
    def get_recent_logins(user):
        """
        Returns the latest login activity.
        """

        return (
            LoginHistory.query.filter_by(
                user_id=user.id
            )
            .order_by(
                LoginHistory.login_time.desc()
            )
            .limit(5)
            .all()
        )

    @staticmethod
    def calculate_security_score(user):
        """
        Calculates the user's security score.
        """

        score = 0

        # Password exists
        if user.password_hash:
            score += 20

        # Email verification
        if user.is_email_verified:
            score += 20

        # Two-factor authentication
        if user.two_factor_enabled:
            score += 30

        # No failed login attempts
        if user.failed_login_attempts == 0:
            score += 15

        # Account not locked
        if user.account_locked_until is None:
            score += 15

        return score

    @staticmethod
    def get_statistics(user):
        """
        Returns dashboard statistics.
        """

        return {

            "login_count": user.login_count,

            "last_login": user.last_login,

            "last_login_ip": user.last_login_ip,

            "failed_attempts": user.failed_login_attempts,

            "email_verified": user.is_email_verified,

            "two_factor_enabled": user.two_factor_enabled,

            "account_locked": (
                user.account_locked_until is not None
            ),

        }