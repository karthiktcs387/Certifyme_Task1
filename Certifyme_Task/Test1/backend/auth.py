import secrets
import re
from datetime import datetime, timezone, timedelta

from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models import Admin, PasswordResetToken

auth_bp = Blueprint('auth', __name__)

EMAIL_RE = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')


# US-1.1 Admin Sign Up
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    full_name = (data.get('full_name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    confirm_password = data.get('confirm_password') or ''

    if not full_name or not email or not password or not confirm_password:
        return jsonify({'error': 'All fields are required.'}), 400

    if not EMAIL_RE.match(email):
        return jsonify({'error': 'Enter a valid email address.'}), 400

    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters.'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Password and confirm password do not match.'}), 400

    if Admin.query.filter_by(email=email).first():
        return jsonify({'error': 'An account with this email already exists.'}), 409

    admin = Admin(
        full_name=full_name,
        email=email,
        password_hash=generate_password_hash(password)
    )
    db.session.add(admin)
    db.session.commit()

    return jsonify({'message': 'Account created successfully.'}), 201


# US-1.2 Admin Login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    remember_me = bool(data.get('remember_me', False))

    admin = Admin.query.filter_by(email=email).first()

    if not admin or not check_password_hash(admin.password_hash, password):
        return jsonify({'error': 'Invalid email or password.'}), 401

    session['admin_id'] = admin.id
    session['admin_email'] = admin.email

    if remember_me:
        session.permanent = True
    else:
        session.permanent = False

    return jsonify({'message': 'Login successful.', 'admin': admin.to_dict()}), 200


# Logout
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Signed out successfully.'}), 200


# US-1.3 Forgot Password
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = (data.get('email') or '').strip().lower()

    if email:
        admin = Admin.query.filter_by(email=email).first()
        if admin:
            token = secrets.token_urlsafe(48)
            expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

            reset_token = PasswordResetToken(
                admin_id=admin.id,
                token=token,
                expires_at=expires_at
            )
            db.session.add(reset_token)
            db.session.commit()

            reset_link = f'http://localhost:5000/api/auth/reset-password/{token}'
            print(f'[PASSWORD RESET] Link for {email}: {reset_link}')

    return jsonify({'message': 'If that email is registered, a reset link has been sent.'}), 200


# Reset Password
@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    reset_token = PasswordResetToken.query.filter_by(token=token, used=False).first()

    if not reset_token or reset_token.is_expired():
        return jsonify({'error': 'This reset link is invalid or has expired.'}), 400

    if request.method == 'GET':
        return jsonify({'message': 'Token is valid. Submit new password.'}), 200

    data = request.get_json()
    new_password = data.get('password') or ''

    if len(new_password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters.'}), 400

    admin = Admin.query.get(reset_token.admin_id)
    admin.password_hash = generate_password_hash(new_password)
    reset_token.used = True
    db.session.commit()

    return jsonify({'message': 'Password reset successfully.'}), 200