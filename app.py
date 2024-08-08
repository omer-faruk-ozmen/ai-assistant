import os
from flask import Flask, flash, g, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from config import Config
from models import db, bcrypt
from routes import app_bp
from services.auth_service import get_current_user as auth_get_current_user
from utils.helpers import get_current_user as helper_get_current_user, get_client_ip

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    app.register_blueprint(app_bp)

    @app.before_request
    def before_request_func():
        g.db = db.session()
        g.current_user = None
        try:
            verify_jwt_in_request(optional=True)
            user_identity = get_jwt_identity()
            if user_identity:
                g.current_user = auth_get_current_user()
        except Exception as e:
            app.logger.error(f"Önceki istek hatası: {e}")

    @app.teardown_request
    def teardown_request_func(exception=None):
        db.session.remove()

    @app.route('/')
    def index():
        current_user = None
        try:
            verify_jwt_in_request(optional=True)
            user_identity = get_jwt_identity()
            if user_identity:
                current_user = auth_get_current_user()
                if current_user and not current_user.is_blocked:
                    return redirect(url_for('app_bp.main_bp.home'))
        except Exception as e:
            app.logger.error(
                f"Hata: {e}", 
                extra={'clientip': get_client_ip(), 'user': helper_get_current_user() or 'unknown'}
            )
            return render_template('index.html', error=str(e))

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
    app.run(host='0.0.0.0', port=port, debug=False)
