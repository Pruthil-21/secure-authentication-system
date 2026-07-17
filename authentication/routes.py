"""
Application routes.
"""

from flask import Blueprint, render_template

# Authentication Blueprint
auth_bp = Blueprint(
    "auth",
    __name__,
)


@auth_bp.route("/")
def home():
    """
    Landing page.
    """
    return render_template("pages/home.html")


@auth_bp.app_errorhandler(404)
def page_not_found(error):
    """
    Custom 404 page.
    """
    return render_template("pages/404.html"), 404