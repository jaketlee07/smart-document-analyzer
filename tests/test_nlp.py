import unittest
from unittest.mock import patch, MagicMock
from flask import url_for, current_app
from app import create_app, db
from app.auth.models import User
from app.uploader.models import UploadedFile
from app.nlp.models import DocumentAnalysis
from tempfile import mkdtemp
import shutil
import os
from datetime import datetime

class TestNLPBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class='app.config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Create a temporary directory for file uploads
        self.temp_dir = mkdtemp()
        self.app.config['UPLOAD_FOLDER'] = self.temp_dir

        # Create a test user
        test_user = User(username='testuser')
        test_user.set_password('testpassword')
        db.session.add(test_user)
        db.session.commit()

        # Simulate file upload
        self.test_file_path = os.path.join(self.temp_dir, 'testfile.pdf')
        with open(self.test_file_path, 'w') as f:
            f.write('Dummy content')

        # Create a test file and link it to the test user
        self.uploaded_file = UploadedFile(user_id=test_user.id, name='testfile.pdf', type='application/pdf', size=os.path.getsize(self.test_file_path), path=self.test_file_path, upload_date=datetime.utcnow())
        db.session.add(self.uploaded_file)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        shutil.rmtree(self.temp_dir)  # Clean up the temporary directory

    @patch('app.nlp.routes.extract_text_from_file')
    @patch('app.nlp.routes.make_openai_request')
    def test_analyze_document_found(self, mock_openai, mock_extract):
        mock_extract.return_value = "This is test document content."
        mock_openai.side_effect = ["Positive", "Brief summary.", "test, document, content"]

        response = self.client.get(url_for('nlp.analyze_document', file_id=self.uploaded_file.id))
        self.assertEqual(response.status_code, 302)  # Expecting redirection after successful processing

        analysis = DocumentAnalysis.query.first()
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.sentiment, "Positive")
        self.assertEqual(analysis.summary, "Brief summary.")
        self.assertEqual(analysis.keywords, "test, document, content")

    def test_analyze_document_not_found(self):
        response = self.client.get(url_for('nlp.analyze_document', file_id=999))
        self.assertEqual(response.status_code, 404)

    @patch('app.nlp.routes.extract_text_from_file')
    def test_no_readable_content(self, mock_extract):
        mock_extract.return_value = None
        response = self.client.get(url_for('nlp.analyze_document', file_id=self.uploaded_file.id))
        self.assertEqual(response.status_code, 422)

    @patch('app.nlp.routes.extract_text_from_file')
    @patch('app.nlp.routes.make_openai_request')
    def test_analysis_failure(self, mock_openai, mock_extract):
        mock_extract.return_value = "This is a test document content."
        mock_openai.return_value = None  # Simulate failure in OpenAI processing

        response = self.client.get(url_for('nlp.analyze_document', file_id=self.uploaded_file.id))
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
