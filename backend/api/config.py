import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

    PROJECT_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OAUTHLIB_INSECURE_TRANSPORT = 1 

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    FLASK_DEBUG = 1
    DEVELOPMENT = True
    TESTING = True

class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    FLASK_DEBUG = 0
    DEVELOPMENT = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}


