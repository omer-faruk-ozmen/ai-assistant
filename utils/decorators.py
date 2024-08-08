from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify

def jwt_required_with_redirect(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except:
            return jsonify(msg="Missing or invalid token"), 401
        return fn(*args, **kwargs)
    return decorator

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_identity()
            if claims['role'] != role:
                return jsonify(msg="Unauthorized"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
