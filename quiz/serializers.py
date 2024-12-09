from rest_framework import serializers
from .models import Quiz, Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'question_type', 'text', 'points', 
                 'options', 'word_select_text']
        
        # set options or word_select_text based on question_type
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.question_type == Question.WORD_SELECT:
            representation.pop('options', None)
        else:
            representation.pop('word_select_text', None)
        return representation

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'questions']