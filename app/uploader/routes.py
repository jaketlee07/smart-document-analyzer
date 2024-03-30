# app/uploader/routes.py
import os
from flask import Blueprint, current_app, request, jsonify
from werkzeug.utils import secure_filename
from .models import db, UploadedFile
from datetime import datetime

uploader_bp = Blueprint('uploader', __name__)

@uploader_bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Add entry to database
        new_file = UploadedFile(
            name=filename,
            type=file.content_type,
            size=os.path.getsize(filepath),
            path=filepath,
            upload_date=datetime.utcnow()
        )
        db.session.add(new_file)
        db.session.commit()

        return jsonify({'message': 'File uploaded successfully', 'file_id': new_file.id}), 200

    return jsonify({'error': 'File type not permitted'}), 400

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
