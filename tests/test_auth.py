import unittest
from flask import Flask, json
from app import create_app, db
from app.auth.models import User
from app.config import TestConfig

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class=TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_registration(self):
        # First registration: should redirect to login, confirming success
        response = self.client.post('/auth/register', data={
            'username': 'testuser1',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)

        # Second registration with the same username: expect 400 due to the username being taken
        response = self.client.post('/auth/register', data={
            'username': 'testuser1',
            'password': 'anotherpassword'
        })
        self.assertEqual(response.status_code, 400)

    def test_user_login(self):
        # First, register a user
        self.client.post('/auth/register', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        # Test a successful login
        response = self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Successful login redirects to upload page

        # Test login with wrong password
        response = self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Render login page again with flash message

if __name__ == '__main__':
    unittest.main()
