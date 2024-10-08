import logging
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_jwt_extended import get_current_user, jwt_required, get_jwt_identity
from services.user_service import change_password, get_current_user_service
from utils.decorators import jwt_required_with_redirect, role_required

logger = logging.getLogger('app')
user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required_with_redirect
def profile():
    current_user = get_jwt_identity()
    logger.info(f"User {current_user['username']} accessed the profile page.")
    return render_template('home.html', username=current_user['username'])


@user_bp.route('/settings', methods=['GET', 'POST'])
@jwt_required()
def settings():
    current_user = get_jwt_identity()
    logger.info(f"User {current_user['username']} accessed the settings page.")

    if request.method == 'POST':
        logger.info(f"User {current_user['username']} is attempting to change password.")
        
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            logger.warning(f"User {current_user['username']} failed password change attempt: Passwords do not match.")
            flash('Yeni şifre ve onay şifresi eşleşmiyor.', 'danger')
            return redirect(url_for('app_bp.user_bp.settings'))

        try:
            current_user = get_current_user_service()

            if not current_user or not current_user.check_password(current_password):
                logger.warning(f"User {current_user.username} failed password change attempt: Incorrect current password.")
                flash('Mevcut şifre hatalı.', 'danger')
                return redirect(url_for('app_bp.user_bp.settings'))

            change_password(current_user.id, new_password)
            logger.info(f"User {current_user.username} successfully changed their password.")
            flash('Şifre başarıyla değiştirildi.', 'success')
            return redirect(url_for('app_bp.user_bp.settings'))

        except Exception as e:
            logger.error(f"Error occurred while changing password for user {current_user.username}: {e}")
            flash('Bir hata oluştu. Lütfen tekrar deneyin.', 'danger')
            return redirect(url_for('app_bp.user_bp.settings'))

    return render_template('settings.html')