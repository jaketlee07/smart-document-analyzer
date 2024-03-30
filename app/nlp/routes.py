# app/nlp/routes.py
from flask import Blueprint, request, jsonify
import spacy

nlp_bp = Blueprint('nlp', __name__)
nlp = spacy.load("en_core_web_sm")

@nlp_bp.route('/analyze', methods=['POST'])
def analyze():
    text = request.json.get('text')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    doc = nlp(text)
    # Extracting entities, for example
    entities = [{'text': entity.text, 'type': entity.label_} for entity in doc.ents]
    
    # You could add more analysis like sentiment, tokens, etc.
    
    # Here you can also store the analysis results in your database if required
    
    return jsonify({'entities': entities}), 200
