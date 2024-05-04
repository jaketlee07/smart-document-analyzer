from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth.models import User
    from .uploader.models import UploadedFile

    # Import and register the blueprints
    from .auth.routes import auth_bp
    from .uploader.routes import uploader_bp
    # from .routes import api_routes  # Updated import
    from .main import home_bp

    app.register_blueprint(home_bp, url_prefix='/')
    # app.register_blueprint(api_routes, url_prefix='/api')  # Updated registration
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(uploader_bp, url_prefix='/uploader')

    with app.app_context():
        User.__table__.create(bind=db.engine, checkfirst=True)
        UploadedFile.__table__.create(bind=db.engine, checkfirst=True)
        # db.create_all()
        # print(db.engine.table_names())
    return app
