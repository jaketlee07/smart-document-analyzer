# app/output_generator/routes.py

from flask import Blueprint, render_template, jsonify
from app import db
from .models import AnalysisOutput
from app.nlp.models import DocumentAnalysis
from datetime import datetime

output_bp = Blueprint('output_generator', __name__, template_folder='templates')

@output_bp.route('/generate/<int:analysis_id>', methods=['GET'])
def generate_output(analysis_id):
    analysis = DocumentAnalysis.query.get(analysis_id)
    if not analysis:
        return jsonify({'error': 'Analysis not found'}), 404

    return render_template('analysis_results.html', analysis=analysis)

# @output_bp.route('/generate/<int:analysis_id>', methods=['GET'])
# def generate_output(analysis_id):
#     analysis = DocumentAnalysis.query.get(analysis_id)
#     if not analysis:
#         return jsonify({'error': 'Analysis not found'}), 404

#     existing_output = AnalysisOutput.query.filter_by(analysis_id=analysis_id).first()
#     if not existing_output:
#         # Format the output with all the data
#         output_text = f"Document: {analysis.uploaded_file.name}\n" \
#                       f"Sentiment Analysis: {analysis.sentiment}\n" \
#                       f"Summary: {analysis.summary}\n" \
#                       f"Details: {analysis.details}"

#         new_output = AnalysisOutput(
#             analysis_id=analysis_id,
#             output_text=output_text,
#             created_at=datetime.utcnow()
#         )
#         db.session.add(new_output)
#         db.session.commit()
#         existing_output = new_output

#     return render_template('analysis_results.html', output=existing_output)
