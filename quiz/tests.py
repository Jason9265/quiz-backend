from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Quiz, Question
from .mongodb import client, DB_NAME, quizzes_collection, questions_collection

class QuizAPITests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Ensure we're using test database
        assert DB_NAME == 'quiz_app_test', "Tests must run against test database!"

    def setUp(self):
        # Clear test collections before each test
        quizzes_collection.delete_many({})
        questions_collection.delete_many({})
        
        # Create test data
        self.quiz_data = {
            'title': 'Test Quiz',
            'description': 'Test Description',
            'pass_score': 70
        }
        result = quizzes_collection.insert_one(self.quiz_data)
        self.quiz_id = str(result.inserted_id)

    def tearDown(self):
        # Clear test collections after each test
        quizzes_collection.delete_many({})
        questions_collection.delete_many({})

    def test_create_quiz(self):
        """Test creating a new quiz"""
        data = {
            'title': 'New Quiz',
            'description': 'New Description',
            'pass_score': 60
        }
        response = self.client.post('/api/quizzes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Quiz')
        
        # Verify in database
        quiz = quizzes_collection.find_one({'title': 'New Quiz'})
        self.assertIsNotNone(quiz)
        self.assertEqual(quiz['description'], 'New Description')

    def test_get_quiz_list(self):
        """Test retrieving quiz list"""
        response = self.client.get('/api/quizzes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Quiz')

    def test_get_quiz_detail(self):
        """Test retrieving quiz detail"""
        response = self.client.get(f'/api/quizzes/{self.quiz_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Quiz')

class QuestionAPITests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        assert DB_NAME == 'quiz_app_test', "Tests must run against test database!"

    def setUp(self):
        # Clear test collections
        quizzes_collection.delete_many({})
        questions_collection.delete_many({})
        
        # Create a test quiz first
        quiz_result = quizzes_collection.insert_one({
            'title': 'Test Quiz',
            'description': 'Test Description',
            'pass_score': 70
        })
        self.quiz_id = str(quiz_result.inserted_id)

    def tearDown(self):
        # Clear test collections
        quizzes_collection.delete_many({})
        questions_collection.delete_many({})

    def test_create_question(self):
        """Test creating a new question"""
        data = {
            'quiz_id': self.quiz_id,
            'question_type': 'single',
            'text': 'Test Question',
            'points': 10,
            'options': {
                'choices': ['A', 'B', 'C'],
                'correct_answer': 'A'
            }
        }
        response = self.client.post('/api/questions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify in database
        question = questions_collection.find_one({'text': 'Test Question'})
        self.assertIsNotNone(question)
        self.assertEqual(question['points'], 10)
