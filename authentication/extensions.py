"""
Initialize Flask extensions.
"""

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# Database
db = SQLAlchemy()

# Password Hashing
bcrypt = Bcrypt()

# User Session Management
login_manager = LoginManager()

# Email Service
mail = Mail()

# CSRF Protection
csrf = CSRFProtect()

# Rate Limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
)