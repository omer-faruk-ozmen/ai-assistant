from flask import Blueprint, flash, request, jsonify, render_template, redirect, session, url_for
from models import db,User
from flask_jwt_extended import create_access_token, current_user, jwt_required, set_access_cookies, unset_jwt_cookies, get_jwt_identity

from services.auth_service import auth_login, auth_register

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        token, error = auth_register(data['username'], data['email'], data['password'])
        if error:
            flash(error, 'danger')
            return redirect(url_for('app_bp.auth_bp.register'))
        response = redirect(url_for('app_bp.main_bp.home'))
        set_access_cookies(response, token)
        return response, 201
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email')
        password = request.form.get('password')
        if not username_or_email or not password:
            flash('Kullanıcı adı/e-posta ve şifre gerekli.', 'danger')
            return redirect(url_for('app_bp.auth_bp.login'))
        
        token, error = auth_login(username_or_email, password)
        if error:
            flash(error, 'danger')
            return redirect(url_for('app_bp.auth_bp.login'))
        
        response = redirect(url_for('app_bp.main_bp.home'))
        set_access_cookies(response, token)
        return response
    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    response = redirect(url_for('index'))
    unset_jwt_cookies(response)
    return response

