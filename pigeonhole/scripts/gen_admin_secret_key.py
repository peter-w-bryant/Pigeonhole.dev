import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Add the parent directory to the path

from app import create_app
from utils.auth import bcrypt
from utils.db import db


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
        verify_secret_key = input('Verify your admin secret key: ')

        if secret_key == verify_secret_key and add_admin_secret_key(secret_key):
            print('Admin secret key added successfully!')
        else:
            print('Admin secret key not added!')