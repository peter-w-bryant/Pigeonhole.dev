import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db" # database file path
    PROJECT_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # project base directory
    OAUTHLIB_INSECURE_TRANSPORT = 1 # allow insecure transport for testing

    # Auth Tokens
    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    FLASK_DEBUG = 1
    DEVELOPMENT = True
    JWT_SECRET_KEY = "secret_for_test_environment"
    SECRET_KEY = "secret_for_test_environment"

class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

# Dictionary of config classes
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}


