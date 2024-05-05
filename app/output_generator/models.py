# app/output_generator/models.py

from app import db
from datetime import datetime

class AnalysisOutput(db.Model):
    __tablename__ = 'analysis_output'

    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('document_analysis.id'), nullable=False)
    analysis = db.relationship('DocumentAnalysis', back_populates='outputs')
    output_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
