import re
from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request
from flask import jsonify
from models import User,db
from flask_jwt_extended.exceptions import NoAuthorizationError

def create_token(user):
    token = create_access_token(identity={'id': user.id, 'username': user.username, 'role': user.role})
    return token

def get_current_user():
    user_identity = get_jwt_identity()
    return User.query.get(user_identity['id'])

def auth_register(username, email, password):
    existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
    if existing_user:
        return None, "E-posta veya kullanıcı adı zaten mevcut"
    
    verify_username = re.match("^[a-zA-Z0-9]+$", username)

    if not verify_username :
        return None,"Kullanıcı adı uygun değil! Sadece harf, rakam barındırabilir ve boşluk bulunmamalı."
        
    
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    token = create_access_token(identity={'id': new_user.id, 'username': new_user.username, 'role': 'user'})
    return token, None

def auth_login(username_or_email, password):
    username_or_email = username_or_email.lower()
    user = User.query.filter(
        (User.email.ilike(username_or_email)) | 
        (User.username.ilike(username_or_email))
    ).first()
    if not user:
        return None, "Kullanıcı bulunamadı veya şifre yanlış!"
    if not user.check_password(password):
        return None, "Kullanıcı bulunamadı veya şifre yanlış!"
    if user.is_blocked ==True:
        return None, "Kullanıcı engelli giriş yapamazsınız!"


    token = create_access_token(identity={'id': user.id, 'username': user.username, 'role': user.role})
    return token, None