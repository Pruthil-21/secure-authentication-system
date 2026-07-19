"""
Login history model.
"""

from datetime import datetime

from authentication.extensions import db


class LoginHistory(db.Model):
    """
    Stores user login attempts.
    """

    __tablename__ = "login_history"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    login_time = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    ip_address = db.Column(
        db.String(45),
        nullable=False,
    )

    browser = db.Column(
        db.String(120),
        nullable=True,
    )

    operating_system = db.Column(
        db.String(120),
        nullable=True,
    )

    successful = db.Column(
        db.Boolean,
        nullable=False,
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "login_history",
            lazy=True,
        ),
    )