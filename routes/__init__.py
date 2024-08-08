from flask import Blueprint

from .auth import auth_bp
from .admin import admin_bp
from .user import user_bp
from .patient import patient_bp
from .main import main_bp

app_bp = Blueprint('app_bp', __name__)

app_bp.register_blueprint(auth_bp, url_prefix='/auth')
app_bp.register_blueprint(admin_bp, url_prefix='/admin')
app_bp.register_blueprint(user_bp, url_prefix='/user')
app_bp.register_blueprint(patient_bp, url_prefix='/patient')
app_bp.register_blueprint(main_bp,url_prefix='')