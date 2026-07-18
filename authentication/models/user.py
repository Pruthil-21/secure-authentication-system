"""
User database model.
"""

from datetime import datetime

from flask_login import UserMixin

from authentication.extensions import db


class User(UserMixin, db.Model):
    """
    User model.
    """

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    full_name = db.Column(
        db.String(100),
        nullable=False,
    )

    username = db.Column(
        db.String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False,
    )

    is_email_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    two_factor_enabled = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self):

        return f"<User {self.username}>"