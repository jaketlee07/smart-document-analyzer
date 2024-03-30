import os
import unittest
from werkzeug.datastructures import FileStorage
from app import create_app, db

class UploaderTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class='TestConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_file_upload(self):
        # Create a dummy file to upload
        data = {
            'file': (BytesIO(b'This is a test file'), 'test.txt')
        }
        response = self.client.post('/uploader/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('message', json_data)
        self.assertEqual(json_data['message'], 'File uploaded successfully')

if __name__ == '__main__':
    unittest.main()
