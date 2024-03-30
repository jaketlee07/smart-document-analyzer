from flask import Blueprint, request, jsonify
# Adjusted import paths to reflect the new structure
from app.queues.tasks import task_queue, process_pdf_function, perform_nlp_analysis

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)

@main.route('/submit/pdf', methods=['POST'])
def submit_pdf():
    """
    Endpoint to submit a PDF processing task.
    Expects 'pdf_path' in form data.
    """
    pdf_path = request.form.get('pdf_path')
    if not pdf_path:
        return jsonify({"error": "PDF path is required."}), 400
    
    # Enqueue the PDF processing task
    task_queue.put((process_pdf_function, [pdf_path]))
    return jsonify({"message": "PDF processing task submitted."}), 202

@main.route('/submit/text', methods=['POST'])
def submit_text():
    """
    Endpoint to submit a text for NLP analysis.
    Expects 'text' in form data.
    """
    text = request.form.get('text')
    if not text:
        return jsonify({"error": "Text is required."}), 400
    
    # Enqueue the NLP analysis task
    task_queue.put((perform_nlp_analysis, [text]))
    return jsonify({"message": "Text analysis task submitted."}), 202

# Assuming `app/__init__.py` is correctly setting up the Flask app and registering the `main` blueprint
