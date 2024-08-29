from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from utils.decorators import role_required
import logging

logger = logging.getLogger('app')

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/home')
@jwt_required()
def home():
    current_user = get_jwt_identity()
    logger.info(f"User {current_user['username']} with role {current_user['role']} accessed the home page.")
    
    try:
        return render_template('home.html', current_username=current_user['username'], current_role=current_user['role'])
    except Exception as e:
        logger.error(f"Error rendering home page for user {current_user['username']}: {e}")
        return render_template('error.html', error_message=str(e)), 500


@main_bp.route('/about')
@jwt_required()
def about():
    current_user = get_jwt_identity()
    logger.info(f"User {current_user['username']} accessed the about page.")
    
    try:
        return render_template('about.html')
    except Exception as e:
        logger.error(f"Error rendering about page for user {current_user['username']}: {e}")
        return render_template('error.html', error_message=str(e)), 500
