from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Quiz, Question
from .serializers import QuizSerializer, QuestionSerializer
from bson import ObjectId
from .mongodb import quizzes_collection, questions_collection

class QuizViewSet(viewsets.ViewSet):
    """
    CRUD endpoints for Quiz:
    list: GET /api/quizzes/
    retrieve: GET /api/quizzes/{id}/
    create: POST /api/quizzes/
    update: PUT /api/quizzes/{id}/
    partial_update: PATCH /api/quizzes/{id}/
    delete: DELETE /api/quizzes/{id}/
    """
    def list(self, request):
        quizzes = list(quizzes_collection.find())
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        quiz = quizzes_collection.find_one({'_id': ObjectId(pk)})
        if not quiz:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Get questions for this quiz
        questions = list(questions_collection.find({'quiz_id': ObjectId(pk)}))
        quiz['questions'] = questions
        
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    def create(self, request):
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            quiz_id = Quiz.create_quiz(**serializer.validated_data)
            quiz = quizzes_collection.find_one({'_id': ObjectId(quiz_id)})
            return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionViewSet(viewsets.ViewSet):
    """
    CRUD endpoints for Quiz:
    list: GET /api/questions/
    retrieve: GET /api/questions/{id}/
    create: POST /api/questions/
    update: PUT /api/questions/{id}/
    partial_update: PATCH /api/questions/{id}/
    delete: DELETE /api/questions/{id}/
    """
    def list(self, request):
        quiz_id = request.query_params.get('quiz_id')
        filter_params = {'quiz_id': ObjectId(quiz_id)} if quiz_id else {}
        questions = list(questions_collection.find(filter_params))
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question_id = Question.create_question(**serializer.validated_data)
            question = questions_collection.find_one({'_id': ObjectId(question_id)})
            return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)