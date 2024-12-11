from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class QuizHistorySerializer(serializers.Serializer):
    id = serializers.CharField(source='_id', read_only=True)
    user_name = serializers.CharField()
    quiz_id = serializers.CharField()
    total_points = serializers.IntegerField()
    earned_points = serializers.IntegerField()
    percentage = serializers.FloatField()
    passed = serializers.BooleanField()
    results = serializers.ListField()
    title = serializers.CharField()
    quiz_time = serializers.DateTimeField(required=False) 