"""
Authentication service.
"""

from authentication.extensions import bcrypt, db
from authentication.models import User
from authentication.validators.password_validator import validate_password


class AuthService:
    """
    Handles authentication business logic.
    """

    @staticmethod
    def register_user(form):

     email = form.email.data.strip().lower()
     username = form.username.data.strip()

     print("=" * 50)
     print("REGISTER ATTEMPT")
     print("Username:", username)
     print("Email:", email)

     existing_email = User.query.filter_by(email=email).first()
     existing_username = User.query.filter_by(username=username).first()

     print("Existing Email:", existing_email)
     print("Existing Username:", existing_username)

     if existing_email:
        print("EMAIL ALREADY EXISTS")
        return False, "An account with this email already exists."

     if existing_username:
        print("USERNAME ALREADY EXISTS")
        return False, "Username is already taken."

        
        email = form.email.data.strip().lower()

        username = form.username.data.strip()

        # Check existing email
        if User.query.filter_by(email=email).first():

         return False, "An account with this email already exists."

        # Check existing username
        if User.query.filter_by(username=username).first():

         return False, "Username is already taken."

        # Validate password
        password_result = validate_password(form.password.data)

        if not password_result.valid:

            return False, password_result.errors[0]

        # Hash password
        password_hash = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        # Create user
        user = User(

            full_name=form.full_name.data.strip(),

            username=form.username.data.strip(),

            email=form.email.data.strip().lower(),

            password_hash=password_hash,

        )

        db.session.add(user)

        db.session.commit()

        return True, "Account created successfully."