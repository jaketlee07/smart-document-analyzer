import os

class Config:
    """Set Flask configuration variables from .env file."""

    # General Config
    SECRET_KEY = 'your_secret_key_here'
    FLASK_APP = 'run.py'
    FLASK_ENV = 'development'

    # Database
    SQLALCHEMY_DATABASE_URI = 'postgresql://jake:jake2002@localhost:5432/smartdocumentanalyzerdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploader Config
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


class TestConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory database for tests
    # Other testing-specific configurations

    # Uploader Config
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

