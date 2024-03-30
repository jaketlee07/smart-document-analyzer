from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_class):
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize plugins
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from .queues import tasks
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        # Include our Routes
        from .auth.routes import auth_bp
        from .uploader.routes import uploader_bp
        # from .nlp.routes import nlp_bp


        # Register Blueprints
        app.register_blueprint(main_blueprint)
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(uploader_bp, url_prefix='/uploader')
        # app.register_blueprint(nlp_bp, url_prefix='/nlp')

        # Create tables for our models
        db.create_all()

        return app
