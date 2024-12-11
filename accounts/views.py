from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, QuizHistory
from .serializers import UserSerializer, LoginSerializer, QuizHistorySerializer

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Check if username exists
        if User.get_user(username):
            return Response(
                {'error': 'Username already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user
        user_id = User.create_user(username, password)
        if user_id:
            return Response({
                'id': user_id,
                'username': username,
                'message': 'User created successfully'
            }, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Check user credentials
        user = User.get_user(username)
        if user and user['password'] == password:
            return Response({
                'id': str(user['_id']),
                'username': user['username'],
                'message': 'Login successful'
            })
        
    return Response(
        {'error': 'Invalid credentials'}, 
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['POST'])
def create_quiz_history(request):
    serializer = QuizHistorySerializer(data=request.data)
    if serializer.is_valid():
        history_id = QuizHistory.create_history(**serializer.validated_data)
        if history_id:
            return Response({
                'id': history_id,
                'message': 'Quiz history created successfully'
            }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_quiz_history(request, username):
    history = QuizHistory.get_user_history(username)

    for item in history:
        item['_id'] = str(item['_id'])
    return Response(history)

@api_view(['GET'])
def get_quiz_history(request, quiz_id):
    history = QuizHistory.get_quiz_history(quiz_id)

    for item in history:
        item['_id'] = str(item['_id'])
    return Response(history)
