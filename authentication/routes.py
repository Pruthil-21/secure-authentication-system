"""
Application routes.
"""

from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from authentication.forms import (
    LoginForm,
    RegistrationForm,
)

from authentication.forms.profile_forms import (
    UpdateProfileForm,
)

from authentication.models import (
    LoginHistory,
    User,
)

from authentication.services import (
    AuthService,
)

from authentication.services.dashboard_service import (
    DashboardService,
)

from authentication.services.profile_service import (
    ProfileService,
)

auth_bp = Blueprint(
    "auth",
    __name__,
)


# ==========================================================
# Home
# ==========================================================

@auth_bp.route("/")
def home():

    return render_template(
        "pages/home.html",
    )


# ==========================================================
# Register
# ==========================================================

@auth_bp.route(
    "/register",
    methods=["GET", "POST"],
)
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        success, message = AuthService.register_user(
            form,
        )

        if success:

            flash(
                message,
                "success",
            )

            return redirect(
                url_for("auth.login")
            )

        flash(
            message,
            "danger",
        )

    return render_template(
        "pages/register.html",
        form=form,
    )


# ==========================================================
# Username Availability API
# ==========================================================

@auth_bp.route("/check-username")
def check_username():

    username = request.args.get(
        "username",
        "",
    ).strip()

    if len(username) < 3:

        return jsonify(
            available=False,
            message="Username is too short.",
        )

    exists = User.query.filter_by(
        username=username,
    ).first()

    return jsonify(
        available=not bool(exists),
        message=(
            "Username is available."
            if not exists
            else "Username already exists."
        ),
    )


# ==========================================================
# Email Availability API
# ==========================================================

@auth_bp.route("/check-email")
def check_email():

    email = request.args.get(
        "email",
        "",
    ).strip().lower()

    exists = User.query.filter_by(
        email=email,
    ).first()

    return jsonify(
        available=not bool(exists),
        message=(
            "Email is available."
            if not exists
            else "An account with this email already exists."
        ),
    )


# ==========================================================
# Login
# ==========================================================

@auth_bp.route(
    "/login",
    methods=["GET", "POST"],
)
def login():

    form = LoginForm()

    if form.validate_on_submit():

        success, message, user = AuthService.login_user(
            form,
            request,
        )

        if success:

            login_user(
                user,
                remember=form.remember.data,
            )

            flash(
                "Welcome back!",
                "success",
            )

            return redirect(
                url_for("auth.dashboard")
            )

        flash(
            message,
            "danger",
        )

    return render_template(
        "pages/login.html",
        form=form,
    )
# ==========================================================
# Profile
# ==========================================================

@auth_bp.route(
    "/profile",
    methods=["GET", "POST"],
)
@login_required
def profile():
    """
    Display and update the authenticated user's profile.
    """

    form = UpdateProfileForm()

    form.current_user = current_user

    if form.validate_on_submit():

        changes = ProfileService.update_profile(
            current_user,
            form,
        )

        if changes:

            flash(
                (
                    "Profile updated successfully. "
                    "Updated: "
                    + ", ".join(changes)
                ),
                "success",
            )

        else:

            flash(
                "No changes were made.",
                "info",
            )

        return redirect(
            url_for("auth.profile")
        )

    if request.method == "GET":

        ProfileService.populate_form(
            form,
            current_user,
        )

    profile_data = ProfileService.get_profile_data(
        current_user,
    )

    return render_template(
        "pages/profile.html",
        form=form,
        profile=profile_data,
    )


# ==========================================================
# Dashboard
# ==========================================================

@auth_bp.route("/dashboard")
@login_required
def dashboard():
    """
    User dashboard.
    """

    dashboard_data = DashboardService.get_dashboard_data(
        current_user,
    )

    return render_template(
        "pages/dashboard.html",
        **dashboard_data,
    )


# ==========================================================
# Logout
# ==========================================================

@auth_bp.route("/logout")
@login_required
def logout():
    """
    Log out the current user.
    """

    logout_user()

    flash(
        "You have been logged out successfully.",
        "success",
    )

    return redirect(
        url_for("auth.login")
    )


# ==========================================================
# Forgot Password
# ==========================================================

@auth_bp.route("/forgot-password")
def forgot_password():

    return render_template(
        "pages/forgot_password.html",
    )


# ==========================================================
# Reset Password
# ==========================================================

@auth_bp.route("/reset-password")
def reset_password():

    return render_template(
        "pages/reset_password.html",
    )


# ==========================================================
# Security Center
# ==========================================================

@auth_bp.route("/security-center")
@login_required
def security_center():

    return render_template(
        "pages/security_center.html",
    )


# ==========================================================
# Verify Email
# ==========================================================

@auth_bp.route("/verify-email")
def verify_email():

    return render_template(
        "pages/verify_email.html",
    )


# ==========================================================
# Verify Login OTP
# ==========================================================

@auth_bp.route("/verify-login-otp")
def verify_login_otp():

    return render_template(
        "pages/verify_login_otp.html",
    )