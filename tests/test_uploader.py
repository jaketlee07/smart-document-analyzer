import os
import unittest
from werkzeug.datastructures import FileStorage
from app import create_app, db
from app.config import TestConfig
from io import BytesIO
from unittest.mock import patch
from flask_login import UserMixin

class MockUser(UserMixin):
    def __init__(self, id):
        self.id = id

class UploaderTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class=TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('flask_login.utils._get_user')
    def test_file_upload(self, mock_current_user):
        mock_user = MockUser(id=1)  # Assuming 1 is a valid user ID in your test database
        mock_current_user.return_value = mock_user

        # Create a dummy file to upload
        data = {
            'file': (BytesIO(b'This is a test file'), 'test.txt')
        }
        response = self.client.post('/uploader/upload', data=data, content_type='multipart/form-data')
        print("Response Status Code:", response.status_code)  # Debugging output
        print("Response Data:", response.data.decode())  # Assuming response data is in bytes, decode to str
        print("Response Headers:", response.headers)  # Inspect headers for location

        self.assertEqual(response.status_code, 302)
        self.assertIn('/nlp/analyze/1', response.location)  # Update this line to match the correct redirect URL

if __name__ == '__main__':
    unittest.main()
