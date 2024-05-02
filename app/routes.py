# # app/routes.py
# from flask import Blueprint, request, jsonify
# from app.queues.tasks import task_queue, process_pdf_function, perform_nlp_analysis

# # Blueprint for API routes handling tasks
# api_routes = Blueprint('api_routes', __name__)

# @api_routes.route('/submit/pdf', methods=['POST'])
# def submit_pdf():
#     """
#     Endpoint to submit a PDF processing task.
#     Expects 'pdf_path' in form data.
#     """
#     pdf_path = request.form.get('pdf_path')
#     if not pdf_path:
#         return jsonify({"error": "PDF path is required."}), 400
    
#     # Enqueue the PDF processing task
#     task_queue.put((process_pdf_function, [pdf_path]))
#     return jsonify({"message": "PDF processing task submitted."}), 202

# @api_routes.route('/submit/text', methods=['POST'])
# def submit_text():
#     """
#     Endpoint to submit a text for NLP analysis.
#     Expects 'text' in form data.
#     """
#     text = request.form.get('text')
#     if not text:
#         return jsonify({"error": "Text is required."}), 400
    
#     # Enqueue the NLP analysis task
#     task_queue.put((perform_nlp_analysis, [text]))
#     return jsonify({"message": "Text analysis task submitted."}), 202
