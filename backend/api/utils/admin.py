from flask import request, jsonify
from functools import wraps
from utils.models import Users, AdminSecretKeys
from utils.auth import bcrypt, login_manager

def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Check if user is an admin
        if not is_admin(request):
            return jsonify({'status': 'error', 'message': 'Admin access required'}), 401
        return f(*args, **kwargs)
    return decorated

def is_admin(request):
    # Check user table for admin username and check password
    user = Users.query.filter_by(username=request.json['username']).first()
    if user is None:
        return False
    if user.check_password(request.json['password']):
        if user.is_admin:
            return True
    return False

def verify_admin_secret_key(secret_key):
    hashed_admin_secret_keys = AdminSecretKeys.query.all()
    for hashed_key in hashed_admin_secret_keys:
        admin_secret_key = bcrypt.check_password_hash(hashed_key.hashed_secret_key, secret_key)
    return admin_secret_key