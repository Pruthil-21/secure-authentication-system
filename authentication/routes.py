"""
Application routes.
"""

from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    session,
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

from authentication.forms.forgot_password_form import (
    ForgotPasswordForm,
)

from authentication.forms.reset_password_form import (
    ResetPasswordForm,
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
    TokenService,
)

from authentication.services.dashboard_service import (
    DashboardService,
)

from authentication.services.profile_service import (
    ProfileService,
)

from authentication.forms.resend_verification_form import (
    ResendVerificationForm,
)

from authentication.services.two_factor_service import (
    TwoFactorService,
)

from authentication.forms.enable_two_factor_form import (
    EnableTwoFactorForm,
)

from authentication.forms.disable_two_factor_form import (
    DisableTwoFactorForm,
)

from authentication.forms.verify_two_factor_form import (
    VerifyTwoFactorForm,
)

from authentication.forms.change_password_form import (
    ChangePasswordForm,
)

from authentication.extensions import (
    bcrypt,
    db,
)

import io
import base64

import qrcode

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

            if user.two_factor_enabled:

                session["pending_2fa_user_id"] = user.id

                session["remember_me"] = form.remember.data

                return redirect(
                    url_for("auth.verify_two_factor")
                )

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
# Verify Two-Factor Authentication
# ==========================================================

@auth_bp.route(
    "/verify-2fa",
    methods=["GET", "POST"],
)
def verify_two_factor():
    """
    Verify the 2FA code before logging in.
    """

    user_id = session.get(
        "pending_2fa_user_id",
    )

    if not user_id:

        flash(
            "Your login session has expired. Please sign in again.",
            "warning",
        )

        return redirect(
            url_for("auth.login")
        )

    user = User.query.get(
        user_id,
    )

    if user is None:

        session.pop(
            "pending_2fa_user_id",
            None,
        )

        session.pop(
            "remember_me",
            None,
        )

        flash(
            "Invalid login session.",
            "danger",
        )

        return redirect(
            url_for("auth.login")
        )

    form = VerifyTwoFactorForm()

    if form.validate_on_submit():

        if TwoFactorService.verify_code(

            user.two_factor_secret,

            form.otp_code.data,

        ):

            login_user(

                user,

                remember=session.get(
                    "remember_me",
                    False,
                ),

            )

            session.pop(
                "pending_2fa_user_id",
                None,
            )

            session.pop(
                "remember_me",
                None,
            )

            flash(
                "Welcome back!",
                "success",
            )

            return redirect(
                url_for("auth.dashboard")
            )

        flash(
            "Invalid authentication code.",
            "danger",
        )

    return render_template(
        "pages/verify_2fa.html",
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
# Login History
# ==========================================================

@auth_bp.route("/login-history")
@login_required
def login_history():
    """
    Display the user's login history.
    """

    history = (
        LoginHistory.query.filter_by(
            user_id=current_user.id,
        )
        .order_by(
            LoginHistory.login_time.desc()
        )
        .all()
    )

    return render_template(
        "pages/login_history.html",
        history=history,
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

@auth_bp.route(
    "/forgot-password",
    methods=["GET", "POST"],
)
def forgot_password():
    """
    Request a password reset email.
    """

    form = ForgotPasswordForm()

    if form.validate_on_submit():

        success, message = AuthService.forgot_password(
            form.email.data,
        )

        flash(
            message,
            "info" if success else "danger",
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "pages/forgot_password.html",
        form=form,
    )
    
# ==========================================================
# Resend Verification Email
# ==========================================================

@auth_bp.route(
    "/resend-verification",
    methods=["GET", "POST"],
)
def resend_verification():
    """
    Resend an email verification link.
    """

    form = ResendVerificationForm()

    if form.validate_on_submit():

        success, message = AuthService.resend_verification(
            form.email.data,
        )

        flash(
            message,
            "info" if success else "danger",
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "pages/resend_verification.html",
        form=form,
    )
    
# ==========================================================
# Reset Password
# ==========================================================

@auth_bp.route(
    "/reset-password/<token>",
    methods=["GET", "POST"],
)
def reset_password(token):
    """
    Reset a user's password.
    """

    form = ResetPasswordForm()

    if form.validate_on_submit():

        success, message = AuthService.reset_password(
            token,
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
        "pages/reset_password.html",
        form=form,
    )

# ==========================================================
# Change Password
# ==========================================================

@auth_bp.route(
    "/change-password",
    methods=["GET", "POST"],
)
@login_required
def change_password():
    """
    Change the user's password.
    """

    form = ChangePasswordForm()

    if form.validate_on_submit():

        success, message = AuthService.change_password(
            current_user,
            form,
        )

        flash(
            message,
            "success" if success else "danger",
        )

        if success:

            return redirect(
                url_for("auth.security_center")
            )

    return render_template(
        "pages/change_password.html",
        form=form,
    )

# ==========================================================
# Security Center
# ==========================================================

@auth_bp.route("/security-center")
@login_required
def security_center():
    """
    Display the user's security settings.
    """

    return render_template(
        "pages/security_center.html",
        user=current_user,
    )

# ==========================================================
# Enable Two-Factor Authentication
# ==========================================================

@auth_bp.route(
    "/enable-2fa",
    methods=["GET", "POST"],
)
@login_required
def enable_two_factor():
    """
    Generate and enable Two-Factor Authentication.
    """

    if current_user.two_factor_enabled:

        flash(
            "Two-Factor Authentication is already enabled.",
            "info",
        )

        return redirect(
            url_for("auth.security_center")
        )

    form = EnableTwoFactorForm()

    if not current_user.two_factor_secret:

        current_user.two_factor_secret = (
            TwoFactorService.generate_secret()
        )

        db.session.commit()

    if form.validate_on_submit():

        if TwoFactorService.verify_code(

            current_user.two_factor_secret,

            form.otp_code.data,

        ):

            current_user.two_factor_enabled = True

            db.session.commit()

            flash(
                "Two-Factor Authentication has been enabled successfully.",
                "success",
            )

            return redirect(
                url_for("auth.security_center")
            )

        flash(
            "Invalid verification code. Please try again.",
            "danger",
        )

    provisioning_uri = (
        TwoFactorService.generate_uri(
            current_user,
        )
    )

    qr = qrcode.make(
        provisioning_uri,
    )

    buffer = io.BytesIO()

    qr.save(
        buffer,
        format="PNG",
    )

    qr_code = base64.b64encode(
        buffer.getvalue(),
    ).decode()

    return render_template(
        "pages/enable_2fa.html",
        form=form,
        qr_code=qr_code,
        secret=current_user.two_factor_secret,
    )
    
# ==========================================================
# Disable Two-Factor Authentication
# ==========================================================

@auth_bp.route(
    "/disable-2fa",
    methods=["GET", "POST"],
)
@login_required
def disable_two_factor():
    """
    Disable Two-Factor Authentication.
    """

    if not current_user.two_factor_enabled:

        flash(
            "Two-Factor Authentication is not enabled.",
            "info",
        )

        return redirect(
            url_for("auth.security_center")
        )

    form = DisableTwoFactorForm()

    if form.validate_on_submit():

        success, message = (
            TwoFactorService.disable_two_factor(
                current_user,
                form.password.data,
                form.otp_code.data,
            )
        )

        flash(
            message,
            "success" if success else "danger",
        )

        if success:

            return redirect(
                url_for("auth.security_center")
            )

    return render_template(
        "pages/disable_2fa.html",
        form=form,
    )
    
# ==========================================================
# Verify Email
# ==========================================================

@auth_bp.route("/verify-email/<token>")
def verify_email(token):
    """
    Verify a user's email address.
    """

    email = TokenService.verify_email_token(
        token,
    )

    if email is None:

        flash(
            "Verification link is invalid or has expired.",
            "danger",
        )

        return redirect(
            url_for("auth.login")
        )

    user = User.query.filter_by(
        email=email,
    ).first()

    if user is None:

        flash(
            "Account not found.",
            "danger",
        )

        return redirect(
            url_for("auth.login")
        )

    if user.is_email_verified:

        flash(
            "Your email address is already verified.",
            "info",
        )

        return redirect(
            url_for("auth.login")
        )

    user.is_email_verified = True

    db.session.commit()

    flash(
        "Your email has been verified successfully.",
        "success",
    )

    return redirect(
        url_for("auth.login")
    )


# ==========================================================
# Verify Login OTP
# ==========================================================

@auth_bp.route("/verify-login-otp")
def verify_login_otp():

    return render_template(
        "pages/verify_login_otp.html",
    )
    