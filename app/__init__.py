from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from dotenv import load_dotenv
import openai
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
load_dotenv()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)

    openai.api_key = os.environ.get('OPENAI_API_KEY')

    

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth.models import User
    from .uploader.models import UploadedFile
    from .nlp.models import DocumentAnalysis
    from .output_generator.models import AnalysisOutput



    # Import and register the blueprints
    from .auth.routes import auth_bp
    from .uploader.routes import uploader_bp
    from .nlp.routes import nlp_bp
    from .output_generator.routes import output_bp
    from .main import home_bp

    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(uploader_bp, url_prefix='/uploader')
    app.register_blueprint(nlp_bp, url_prefix='/nlp')
    app.register_blueprint(output_bp, url_prefix='/output')

    with app.app_context():
        UploadedFile.__table__.create(bind=db.engine, checkfirst=True)
        User.__table__.create(bind=db.engine, checkfirst=True)
        DocumentAnalysis.__table__.create(bind=db.engine, checkfirst=True)
        AnalysisOutput.__table__.create(bind=db.engine, checkfirst=True)
        # db.create_all()
        # print(db.engine.table_names())
    return app

