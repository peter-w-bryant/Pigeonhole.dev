from flask_login import LoginManager # for handling user sessions
from flask_bcrypt import Bcrypt # for hashing passwords

# initialize bcrypt and login_manager
bcrypt = Bcrypt() # Bcrypt for hashing passwords
login_manager = LoginManager()


