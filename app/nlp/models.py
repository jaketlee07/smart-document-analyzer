# app/nlp/models.py
from app.uploader.models import db

# If you are storing the analysis results:
class TextAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    entities = db.Column(db.JSON) # Assuming you're storing entities as JSON
    # You could add more fields for other aspects like sentiment, keywords, etc.
