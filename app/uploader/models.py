from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80))
    size = db.Column(db.Integer)
    path = db.Column(db.String(200))
    upload_date = db.Column(db.DateTime)
