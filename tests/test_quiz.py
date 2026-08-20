"""
Unit and API Integration Tests for Heritage Trivia Quiz & Badge Evaluation
"""
import unittest
from flask import Flask
from routes.api import api_bp
from models.quiz import (
    get_all_quiz_questions,
    get_quiz_categories,
    evaluate_quiz_submission
)


class TestQuizModelAndAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.register_blueprint(api_bp, url_prefix='/api/v1')
        cls.client = cls.app.test_client()

    def test_quiz_questions_data(self):
        """Verify presence of heritage trivia questions."""
        questions = get_all_quiz_questions()
        self.assertGreaterEqual(len(questions), 5)
        # Client safe: ensure correct_index is NOT leaked in client safe model
        for q in questions:
            self.assertNotIn('correct_index', q)
            self.assertEqual(len(q['options']), 4)

    def test_quiz_categories(self):
        """Verify categories list."""
        cats = get_quiz_categories()
        self.assertIn('history', cats)
        self.assertIn('culture', cats)
        self.assertIn('archaeology', cats)

    def test_evaluation_scoring_and_badges(self):
        """Verify scoring algorithm and badge assignment."""
        perfect_answers = {
            "q-aryabhata-discovery": 1,
            "q-nalanda-library": 0,
            "q-madhubani-pigment": 1,
            "q-silao-khaja-gi": 1,
            "q-valmiki-river": 1,
            "q-bhikhari-thakur": 1
        }
        res = evaluate_quiz_submission(perfect_answers)
        self.assertEqual(res['score'], 6)
        self.assertEqual(res['percentage'], 100.0)
        self.assertIn('Mahapandit', res['badge'])

        # Empty submission
        res_empty = evaluate_quiz_submission({})
        self.assertEqual(res_empty['score'], 0)
        self.assertEqual(res_empty['percentage'], 0)

    def test_quiz_api_endpoints(self):
        """Test /api/v1/quiz API endpoints."""
        res = self.client.get('/api/v1/quiz/questions')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['count'], 0)

        # Categories API
        res_cat = self.client.get('/api/v1/quiz/categories')
        self.assertEqual(res_cat.status_code, 200)
        self.assertEqual(res_cat.get_json()['status'], 'success')

        # Evaluation POST API
        payload = {
            "answers": {
                "q-aryabhata-discovery": 1,
                "q-nalanda-library": 0
            }
        }
        res_eval = self.client.post('/api/v1/quiz/evaluate', json=payload)
        self.assertEqual(res_eval.status_code, 200)
        eval_data = res_eval.get_json()
        self.assertEqual(eval_data['status'], 'success')
        self.assertEqual(eval_data['evaluation']['score'], 2)


if __name__ == '__main__':
    unittest.main()