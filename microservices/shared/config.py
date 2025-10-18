import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://myuser:mypassword@localhost/myappdb?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Service URLs
    AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL') or 'http://localhost:5001'
    PACKAGE_SERVICE_URL = os.environ.get('PACKAGE_SERVICE_URL') or 'http://localhost:5002'
    MAPS_SERVICE_URL = os.environ.get('MAPS_SERVICE_URL') or 'http://localhost:5003'
    
    # External API Keys
    ORS_API_KEY = os.environ.get("ORS_API_KEY")  # OpenRouteService API Key

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}