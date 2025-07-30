import os

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    # Development-specific settings
    DATABASE_URL = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=GARRY\\SQLEXPRESS;DATABASE=timesheet;Trusted_Connection=yes;'
    APP_NAME = 'Timesheet Dev'
    BASE_URL = 'http://localhost:8080'
    
class UATConfig(Config):
    """UAT configuration"""
    DEBUG = True
    DATABASE_URL = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=GARRY\\SQLEXPRESS;DATABASE=timesheet;Trusted_Connection=yes;'
    APP_NAME = 'UAT Timesheet'
    BASE_URL = 'http://uat-timesheet.local:8080'
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # Production-specific settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'uat': UATConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 