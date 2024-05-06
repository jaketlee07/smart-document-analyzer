from flask import Blueprint, request, jsonify, current_app, redirect, url_for
from app import db
from app.uploader.models import UploadedFile
from app.nlp.models import DocumentAnalysis
from datetime import datetime
import openai
import os
import pdfplumber
import requests

nlp_bp = Blueprint('nlp', __name__, template_folder='../templates')

@nlp_bp.route('/analyze/<int:file_id>', methods=['GET'])
def analyze_document(file_id):
    uploaded_file = UploadedFile.query.get(file_id)
    if not uploaded_file:
        return jsonify({'error': 'File not found'}), 404

    content = extract_text_from_file(uploaded_file.path, uploaded_file.type)
    if not content:
        return jsonify({'error': 'No readable content found in file'}), 422

    sentiment = analyze_sentiment_with_chatgpt(content)
    summary = summarize_text_with_chatgpt(content)
    keywords = extract_keywords_with_chatgpt(content)
    details = f"File Type: {uploaded_file.type}, File Size: {os.path.getsize(uploaded_file.path)}"

    if not sentiment or not summary:
        return jsonify({'error': 'Analysis failed'}), 500

    analysis = DocumentAnalysis(
        uploaded_file_id=file_id,
        sentiment=sentiment,
        summary=summary,
        keywords=keywords,
        details=details,
        created_at=datetime.utcnow()
    )
    db.session.add(analysis)
    db.session.commit()

    return redirect(url_for('output_generator.generate_output', analysis_id=analysis.id))

def extract_text_from_file(path, file_type):
    if file_type == 'application/pdf':
        with pdfplumber.open(path) as pdf:
            return ''.join(page.extract_text() or '' for page in pdf.pages)
    elif file_type == 'text/plain':
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    return None

def make_openai_request(text, prompt):
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("API key is not configured properly.")

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt.format(text=text)}
        ]
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    if response.status_code == 200:
        try:
            return response.json()['choices'][0]['message']['content'].strip()
        except (IndexError, KeyError):
            return None
    return None

def analyze_sentiment_with_chatgpt(text):
    return make_openai_request(text, "Analyze the sentiment of this text: {text}")

def summarize_text_with_chatgpt(text):
    return make_openai_request(text, "Summarize this text: {text}")

def extract_keywords_with_chatgpt(text):
    return make_openai_request(text, "Extract keywords from this text, only give the key words: {text}")

