from flask import Blueprint, flash, request, jsonify, render_template, redirect, session, url_for
from models import db, User
from flask_jwt_extended import create_access_token, current_user, jwt_required, set_access_cookies, unset_jwt_cookies, get_jwt_identity
from services.auth_service import auth_login, auth_register
import logging

logger = logging.getLogger('app')

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        logger.info("User attempted to register.")
        data = request.form
        try:
            token, error = auth_register(data['username'], data['email'], data['password'])
            if error:
                logger.warning(f"Registration failed for user {data['username']}: {error}")
                return jsonify({'success': False, 'error': error}), 400
            
            logger.info(f"User {data['username']} registered successfully.")
            response = jsonify({'success': True, 'redirect_url': url_for('app_bp.main_bp.home')})
            set_access_cookies(response, token)
            return response, 201
        except Exception as e:
            logger.error(f"Error during registration for user {data['username']}: {e}")
            return jsonify({'success': False, 'error': 'Internal server error.'}), 500
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        logger.info("User attempted to log in.")
        username_or_email = request.form.get('username_or_email')
        password = request.form.get('password')

        if not username_or_email or not password:
            logger.warning("Login failed: Username/email or password is missing.")
            flash('Kullanıcı adı/e-posta ve şifre gerekli.', 'danger')
            return redirect(url_for('app_bp.auth_bp.login'))
        
        try:
            token, error = auth_login(username_or_email, password)
            if error:
                logger.warning(f"Login failed for user {username_or_email}: {error}")
                flash(error, 'danger')
                return redirect(url_for('app_bp.auth_bp.login'))
            
            logger.info(f"User {username_or_email} logged in successfully.")
            response = redirect(url_for('app_bp.main_bp.home'))
            set_access_cookies(response, token)
            return response
        except Exception as e:
            logger.error(f"Error during login for user {username_or_email}: {e}")
            flash('Bir hata oluştu. Lütfen tekrar deneyin.', 'danger')
            return redirect(url_for('app_bp.auth_bp.login'))
    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    logger.info(f"User {current_user['username']} logged out.")
    response = redirect(url_for('index'))
    unset_jwt_cookies(response)
    return response
