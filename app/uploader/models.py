#app/uploader/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

class UploadedFile(db.Model):
    __tablename__ = 'uploaded_file'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('uploaded_files', lazy=True))
    #user = db.relationship('User', backref='uploaded_files')
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255))
    size = db.Column(db.Integer)
    path = db.Column(db.String(255))
    upload_date = db.Column(db.DateTime)
    analyses = db.relationship('DocumentAnalysis', back_populates='uploaded_file')
