class Config:
    """Set Flask configuration variables from .env file."""

    # General Config
    SECRET_KEY = 'your_secret_key_here'
    FLASK_APP = 'run.py'
    FLASK_ENV = 'development'

    # Database
    SQLALCHEMY_DATABASE_URI = 'postgresql://jake:jake2002@localhost/smartdocumentanalyzerdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploader Config
    UPLOAD_FOLDER = '/uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

class TestConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory database for tests
    # Other testing-specific configurations

    # Uploader Config
    UPLOAD_FOLDER = '/uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
