import unittest
from flask import json
from app import create_app, db
from app.auth.models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class='TestConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_registration(self):
        # Test a successful registration
        response = self.client.post('/auth/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', data['message'])

        # Test registration with existing username
        response = self.client.post('/auth/register', json={
            'username': 'testuser',
            'password': 'anotherpassword'
        })
        self.assertEqual(response.status_code, 400)

    def test_user_login(self):
        # First, register a user
        self.client.post('/auth/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        # Test a successful login
        response = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)

        # Test login with wrong password
        response = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
