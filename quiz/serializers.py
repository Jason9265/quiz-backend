from rest_framework import serializers
from bson import ObjectId

class QuestionSerializer(serializers.Serializer):
    id = serializers.CharField(source='_id', read_only=True)
    quiz_id = serializers.CharField()
    question_type = serializers.CharField()
    text = serializers.CharField()
    points = serializers.IntegerField()
    options = serializers.DictField(required=False)
    word_select_text = serializers.DictField(required=False)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance['_id'])
        data['quiz_id'] = str(instance['quiz_id'])
        return data

    def validate_options(self, value):
        if 'correct_answer' not in value:
            raise serializers.ValidationError("Options must include a 'correct_answer' field.")
        return value

class QuizSerializer(serializers.Serializer):
    id = serializers.CharField(source='_id', read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    pass_score = serializers.IntegerField()
    questions = QuestionSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance['_id'])
        return data

class QuizAnswerSerializer(serializers.Serializer):
    question_id = serializers.CharField()
    answer = serializers.JSONField() 

class QuizSubmissionSerializer(serializers.Serializer):
    answers = QuizAnswerSerializer(many=True)