from django.db import models
from datetime import datetime
from bson import ObjectId

# These are now just reference classes, not Django models
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    pass_score = models.TextField()

    def __str__(self):
        return self.title

    @staticmethod
    def create_quiz(title, description, pass_score=60, created_by=None):
        from .mongodb import quizzes_collection
        quiz_data = {
            'title': title,
            'description': description,
            'pass_score': pass_score,
        }
        result = quizzes_collection.insert_one(quiz_data)
        return str(result.inserted_id)

    @staticmethod
    def get_quiz(quiz_id):
        from .mongodb import quizzes_collection
        return quizzes_collection.find_one({'_id': ObjectId(quiz_id)})

class Question(models.Model):
    quiz_id = models.TextField()
    question_type = models.TextField()
    text = models.TextField()
    points = models.IntegerField()

    SINGLE_ANSWER = 'single'
    MULTIPLE_ANSWER = 'multiple'
    WORD_SELECT = 'word_select'
    
    QUESTION_TYPES = [
        (SINGLE_ANSWER, 'Single Answer'),
        (MULTIPLE_ANSWER, 'Multiple Answer'),
        (WORD_SELECT, 'Word Select'),
    ]

    @staticmethod
    def create_question(quiz_id, question_type, text, points=1, options=None, word_select_text=None):
        from .mongodb import questions_collection
        if options and 'correct_answer' not in options:
            raise ValueError("Options must include a 'correct_answer' field.")
        
        question_data = {
            'quiz_id': ObjectId(quiz_id),
            'question_type': question_type,
            'text': text,
            'points': points,
            'options': options or {},
            'word_select_text': word_select_text or {}
        }
        result = questions_collection.insert_one(question_data)
        return str(result.inserted_id)
