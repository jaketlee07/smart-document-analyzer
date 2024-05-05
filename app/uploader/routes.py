# app/uploader/routes.py
import os
from flask import Blueprint, current_app, request, jsonify, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from .models import db, UploadedFile
from datetime import datetime

uploader_bp = Blueprint('uploader', __name__)

@uploader_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('uploader_form.html')

    file = request.files.get('file')
    if not file:
        flash('No file part')
        return redirect(url_for('uploader.upload'))

    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('uploader.upload'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'])
        os.makedirs(upload_dir, exist_ok=True)

        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)

        new_file = UploadedFile(
            user_id=current_user.id,
            name=filename,
            type=file.content_type,
            size=os.path.getsize(filepath),
            path=filepath,
            upload_date=datetime.utcnow()
        )
        db.session.add(new_file)
        db.session.commit()

        # Redirect to NLP analysis
        return redirect(url_for('nlp.analyze_document', file_id=new_file.id))

    flash('File type not permitted')
    return redirect(url_for('uploader.upload'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

