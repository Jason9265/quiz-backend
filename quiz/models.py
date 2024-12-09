from djongo import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    pass_score = models.IntegerField(default=60)
    
    class Meta:
        db_table = 'quizzes'

class Question(models.Model):
    SINGLE_ANSWER = 'single'
    MULTIPLE_ANSWER = 'multiple'
    WORD_SELECT = 'word_select'
    
    QUESTION_TYPES = [
        (SINGLE_ANSWER, 'Single Answer'),
        (MULTIPLE_ANSWER, 'Multiple Answer'),
        (WORD_SELECT, 'Word Select'),
    ]
    
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    text = models.TextField()
    points = models.IntegerField(default=1)
    
    options = models.JSONField(default=dict)  # For single/multiple options
    correct_answer = models.JSONField(default=dict)  # Stores correct answers
    
    # For word select options
    word_select_text = models.JSONField(default=dict)  # {text: string, selectable_words: []}
    
    class Meta:
        db_table = 'questions'
