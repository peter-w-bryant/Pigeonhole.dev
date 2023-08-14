import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Add the parent directory to the path

from utils.models import AdminSecretKeys
from utils.auth import bcrypt
from utils.db import db
from app import create_app

def add_admin_secret_key(secret_key):
    hashed_secret_key = bcrypt.generate_password_hash(secret_key)
    admin_secret_key = AdminSecretKeys(hashed_secret_key=hashed_secret_key)
    db.session.add(admin_secret_key)
    db.session.commit()
    return True

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        secret_key = input('Enter admin secret key: ')
        if add_admin_secret_key(secret_key):
            print('Admin secret key added successfully!')
        else:
            print('Admin secret key not added!')