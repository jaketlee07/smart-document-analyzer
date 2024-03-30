import unittest
from app import create_app, db
from app.nlp.routes import nlp

class NLPTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class='TestConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_text_analysis(self):
        test_text = "Apple is looking at buying U.K. startup for $1 billion"
        response = self.client.post('/nlp/analyze', json={'text': test_text})
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue('entities' in json_data)
        self.assertIsInstance(json_data['entities'], list)
        # Assuming your NLP endpoint returns entities
        self.assertGreater(len(json_data['entities']), 0)

if __name__ == '__main__':
    unittest.main()
