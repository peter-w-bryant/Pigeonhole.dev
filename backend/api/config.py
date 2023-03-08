import os

class Config:
    DEBUG = False
    TESTING = False

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

    # MySQL Database
    # MYSQL_USER = os.environ.get('MySQL_USER')
    # MYSQL_PASSWORD = os.environ.get('MySQL_PASSWORD')
    # MYSQL_HOST = os.environ.get('MySQL_HOST')
    # MYSQL_DB = os.environ.get('MySQL_DB')

    # Auth Tokens
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    FLASK_DEBUG = 1
    DEVELOPMENT = True
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


