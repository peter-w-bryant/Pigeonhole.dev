from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from utils.models import Users, AdminSecretKeys
from utils.auth import bcrypt, login_manager

def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_admin():
            return jsonify({'status': 'error', 'message': 'Admin access required'}), 401
        return f(*args, **kwargs)
    return decorated

@jwt_required()
def is_admin():
    user_uid = get_jwt_identity()
    user = Users.query.filter_by(UID=user_uid).first()
    if user is None:
        return False
    if user.is_admin:
        return True
    return False

def verify_admin_secret_key(secret_key):
    hashed_admin_secret_keys = AdminSecretKeys.query.all()
    for hashed_key in hashed_admin_secret_keys:
        admin_secret_key = bcrypt.check_password_hash(hashed_key.hashed_secret_key, secret_key)
    return admin_secret_key