"""
Application factory for the Secure Authentication System.
"""

from pathlib import Path

from flask import Flask

from config import Config
from authentication.extensions import (
    bcrypt,
    csrf,
    db,
    limiter,
    login_manager,
    mail,
)


def create_app():
    """
    Create and configure the Flask application.
    """

    BASE_DIR = Path(__file__).resolve().parent.parent

    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
        instance_path=str(BASE_DIR / "instance"),
    )

    # Load configuration
    app.config.from_object(Config)

    # Initialize Flask extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # Flask-Login configuration
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        """
        Temporary user loader.

        This will be replaced after implementing
        the User model in the registration phase.
        """
        return None

    # Register Blueprints
    from authentication.routes import auth_bp

    app.register_blueprint(auth_bp)

    return app