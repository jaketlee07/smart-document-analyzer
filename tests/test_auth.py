import unittest
from flask import json
from app import create_app, db
from app.auth.models import User
from app.config import TestConfig


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class=TestConfig)
        self.client = self.app.test_client()
        #User.__table__.create(bind=db.engine, checkfirst=True)
        with self.app.app_context():
            #User.__table__.create(bind=db.engine, checkfirst=True)
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_registration(self):
        # Test a successful registration
        response = self.client.post('/auth/register', json={
            'username': 'testuser1',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', json.loads(response.data)['message'])

        # Test registration with an existing username
        response = self.client.post('/auth/register', json={
            'username': 'testuser1',
            'password': 'anotherpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username already taken', json.loads(response.data)['error'])

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
