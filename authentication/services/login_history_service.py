"""
Login history service.
"""

from user_agents import parse

from authentication.extensions import db
from authentication.models import LoginHistory


class LoginHistoryService:
    """
    Handles login history records.
    """

    @staticmethod
    def record_login(user, request, successful):
        """
        Save a login attempt.
        """

        user_agent = parse(request.user_agent.string)

        browser = (
            f"{user_agent.browser.family} "
            f"{user_agent.browser.version_string}"
        ).strip()

        operating_system = (
            f"{user_agent.os.family} "
            f"{user_agent.os.version_string}"
        ).strip()

        login_history = LoginHistory(

            user_id=user.id,

            ip_address=request.remote_addr,

            browser=browser,

            operating_system=operating_system,

            successful=successful,

        )

        db.session.add(login_history)