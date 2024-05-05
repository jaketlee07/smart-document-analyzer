# app/nlp/models.py

from app import db
from datetime import datetime

class DocumentAnalysis(db.Model):
    __tablename__ = 'document_analysis'

    id = db.Column(db.Integer, primary_key=True)
    uploaded_file_id = db.Column(db.Integer, db.ForeignKey('uploaded_file.id'), nullable=False)
    uploaded_file = db.relationship('UploadedFile', back_populates='analyses')
    outputs = db.relationship('AnalysisOutput', back_populates='analysis')
    sentiment = db.Column(db.Text)
    summary = db.Column(db.Text)  # Added summary field here
    keywords = db.Column(db.Text)  # Added keywords field here
    details = db.Column(db.Text)  # For storing detailed analysis
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
