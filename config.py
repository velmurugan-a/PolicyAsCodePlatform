"""
Configuration Module for Policy-as-Code Platform
=================================================
This module contains all configuration settings for the Flask application,
including database settings, JWT configuration, and OPA server settings.
"""

import os
from datetime import timedelta

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base Configuration Class
    Contains default settings used across all environments.
    """
    
    # Flask Secret Key - Used for session management and token signing
    # In production, this should be set via environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY', 'policy-as-code-secret-key-change-in-production')
    
    # SQLite Database Configuration
    # Database file will be stored in the project root
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "pac_platform.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT (JSON Web Token) Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Token expires after 1 hour
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # OPA (Open Policy Agent) Configuration
    # OPA server endpoint - can run locally or as a separate service
    OPA_SERVER_URL = os.environ.get('OPA_SERVER_URL', 'http://localhost:8181')
    OPA_POLICY_PATH = os.path.join(BASE_DIR, 'opa_policies')
    
    # Application Settings
    DEBUG = False
    TESTING = False
    
    # CORS Settings
    CORS_HEADERS = 'Content-Type'


class DevelopmentConfig(Config):
    """
    Development Configuration
    Used during local development with debug mode enabled.
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Log SQL queries for debugging


class ProductionConfig(Config):
    """
    Production Configuration
    Used in production environment with enhanced security.
    """
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # Override with strong secrets in production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')


class TestingConfig(Config):
    """
    Testing Configuration
    Used during automated testing.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


# Configuration dictionary for easy access
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
