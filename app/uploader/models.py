from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

# db = SQLAlchemy()

class UploadedFile(db.Model):
    # __tablename__ = 'uploaded_file'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
