import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:khaleesi@{}/{}".format('localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data= json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_get_all_categories(self):
        response= self.client().get('/categories')
        self.assertEquals(response.status_code,200)

    def test_delete_a_question_fails_with_unprocessable_if_question_does_not_exist(self):
        response= self.client().delete('/questions/1000')
        data= json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertIn('unprocessable', data['message'])

    def test_delete_question_successfully(self):
        response= self.client().delete('/questions/5')
        data= json.loads(response.data)
        question= Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertIn('Question Successfully deleted.', data['message'])

    def test_add_a_question(self):
        new_question= {'question':"What is life", 'answer':'a puzzle', 'difficulty':1, 'category':4 }
        response=self.client().post('/questions', json=new_question)
        data =json.loads(response.data)

        self.assertIn('Question Successfully added.', data['message'])
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 201)
    
    def test_get_questions_by_category(self):
        response=self.client().get('/categories/3/questions')
        data =json.loads(response.data)
        
        self.assertEqual(data['success'],True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()