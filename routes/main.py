from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from utils.decorators import role_required

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/home')
@jwt_required()
def home():
    current_user = get_jwt_identity()
    return render_template('home.html', current_username=current_user['username'],current_role=current_user['role'])


@main_bp.route('/about')
@jwt_required()
def about():
    return render_template('about.html')



