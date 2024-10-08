import logging
import os
from flask import Flask, flash, g, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from jwt import ExpiredSignatureError
from config import Config
from models import db, bcrypt
from routes import app_bp
from services.auth_service import get_current_user as auth_get_current_user
from utils.helpers import _init_logger, get_current_user as helper_get_current_user
_logger = logging.getLogger('app')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    app.register_blueprint(app_bp)
    _init_logger(log_level=logging.INFO)

    @app.before_request
    def before_request_func():
        if request.endpoint in ['app_bp.auth_bp.login', 'static']:
            return
        g.current_user = None
        try:
            verify_jwt_in_request(optional=True)
            user_identity = get_jwt_identity()
            if user_identity:
                g.current_user = auth_get_current_user()
        except Exception as e:
            flash("Oturum süreniz dolmuş. Lütfen tekrar giriş yapın.", "info")
            return redirect(url_for('app_bp.auth_bp.login'))

    @app.teardown_request
    def teardown_request_func(exception=None):
        db.session.remove()

    @app.route('/')
    def index():
        try:
            verify_jwt_in_request(optional=True)
            user_identity = get_jwt_identity()
            if user_identity:
                current_user = auth_get_current_user()
                if current_user and not current_user.is_blocked:
                    return redirect(url_for('app_bp.main_bp.home'))
        except Exception:
            flash("Bir hata oluştu. Lütfen tekrar giriş yapın.", "error")
            return redirect(url_for('app_bp.auth_bp.login'))

        return render_template('index.html')

    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        flash("Bu sayfaya erişmek için yetkiniz yok. Lütfen giriş yapın.", "info")
        return redirect(url_for('app_bp.auth_bp.login'))

    @jwt.expired_token_loader
    def expired_token_callback(header, payload):
        flash("Oturum süreniz doldu. Lütfen tekrar giriş yapın.", "info")
        return redirect(url_for('app_bp.auth_bp.login'))
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 8080))  
    _logger.info('App started in %s', os.getcwd())
    app.run(host='0.0.0.0', port=port, debug=False)
