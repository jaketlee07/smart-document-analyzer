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




# from flask import Blueprint, request, jsonify, current_app, redirect, url_for
# from app import db
# from app.uploader.models import UploadedFile
# from app.nlp.models import DocumentAnalysis
# from datetime import datetime
# import openai
# import os
# import pdfplumber
# import requests

# nlp_bp = Blueprint('nlp', __name__, template_folder='../templates')

# @nlp_bp.route('/analyze/<int:file_id>', methods=['GET'])
# def analyze_document(file_id):
#     uploaded_file = UploadedFile.query.get(file_id)
#     if not uploaded_file:
#         return jsonify({'error': 'File not found'}), 404

#     content = extract_text_from_file(uploaded_file.path, uploaded_file.type)
#     if not content:
#         return jsonify({'error': 'No readable content found in file'}), 422

#     analysis_results = analyze_text_with_chatgpt(content)
#     if 'error' in analysis_results:
#         return jsonify({'error': analysis_results['error']}), 500

#     # Save the analysis result in the database
#     analysis = DocumentAnalysis(
#         uploaded_file_id=file_id,
#         sentiment=analysis_results['sentiment'],
#         summary=analysis_results['summary'],
#         details="Detailed analysis provided by ChatGPT",
#         created_at=datetime.utcnow()
#     )
#     db.session.add(analysis)
#     db.session.commit()

#     return redirect(url_for('output_generator.generate_output', analysis_id=analysis.id))

# def extract_text_from_file(path, file_type):
#     if file_type == 'application/pdf':
#         with pdfplumber.open(path) as pdf:
#             return ''.join(page.extract_text() or '' for page in pdf.pages)
#     elif file_type == 'text/plain':
#         with open(path, 'r', encoding='utf-8') as file:
#             return file.read()
#     return None

# def analyze_text_with_chatgpt(text):
#     api_key = os.environ.get('OPENAI_API_KEY')  # Ensure your API key is set in the environment variables
#     headers = {
#         'Authorization': f'Bearer {api_key}',
#         'Content-Type': 'application/json',
#     }
#     data = {
#         'model': 'gpt-3.5-turbo',
#         'messages': [
#             {'role': 'system', 'content': 'You are a helpful assistant.'},
#             {'role': 'user', 'content': f"Analyze the sentiment of this text: {text}"},
#             {'role': 'user', 'content': f"Summarize this text: {text}"}
#         ]
#     }
#     response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
#     if response.status_code == 200:
#         try:
#             responses = response.json()['choices'][0]['message']['content'].strip().split('\n')
#             sentiment = responses[0]  # Assuming the sentiment analysis result is in the first line
#             summary = responses[1] if len(responses) > 1 else ''  # Assuming the summary is in the second line
#             return {'sentiment': sentiment, 'summary': summary}
#         except (IndexError, KeyError):
#             return {'error': "Failed to parse response."}
#     return {'error': f"Failed to contact API: {response.text}"}

# def find_keywords_with_chatgpt(text):
#     api_key = os.environ.get('OPENAI_API_KEY')  # Ensure your API key is set in the environment variables
#     headers = {
#         'Authorization': f'Bearer {api_key}',
#         'Content-Type': 'application/json',
#     }
#     data = {
#         'model': 'gpt-3.5-turbo',
#         'messages': [
#             {'role': 'system', 'content': 'You are a helpful assistant.'},
#             {'role': 'user', 'content': f"Analyze the sentiment of this text: {text}"},
#             {'role': 'user', 'content': f"Summarize this text: {text}"}
#         ]
#     }
#     response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
#     if response.status_code == 200:
#         try:
#             responses = response.json()['choices'][0]['message']['content'].strip().split('\n')
#             sentiment = responses[0]  # Assuming the sentiment analysis result is in the first line
#             summary = responses[1] if len(responses) > 1 else ''  # Assuming the summary is in the second line
#             return {'sentiment': sentiment, 'summary': summary}
#         except (IndexError, KeyError):
#             return {'error': "Failed to parse response."}
#     return {'error': f"Failed to contact API: {response.text}"}