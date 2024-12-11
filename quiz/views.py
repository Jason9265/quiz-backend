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
    submit: POST /api/quizzes/{id}/submit/
    attempt: GET /api/quizzes/{id}/attempt/
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
        
        # Get questions for this quiz matching the quiz_id
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

    # endpoint for answer submission
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        quiz = quizzes_collection.find_one({'_id': ObjectId(pk)})
        if not quiz:
            return Response(status=status.HTTP_404_NOT_FOUND)

        questions = list(questions_collection.find({'quiz_id': ObjectId(pk)}))
        
        total_points = 0
        earned_points = 0
        results = []

        submitted_answers = request.data.get('answers', [])
        
        for answer in submitted_answers:
            question_id = answer.get('question_id')
            submitted_answer = answer.get('answer')
            
            question = next(
                (q for q in questions if str(q['_id']) == question_id), 
                None
            )
            
            if not question:
                continue

            total_points += question['points']
            is_correct = False
            
            if question['question_type'] == 'single':
                is_correct = (
                    submitted_answer == question['options']['correct_answer']
                )
            else:
                correct_words = set(question['options']['correct_answer'])
                submitted_set = set(submitted_answer if isinstance(submitted_answer, list) else [submitted_answer])
                is_correct = correct_words == submitted_set

            if is_correct:
                earned_points += question['points']

            results.append({
                'question_id': question_id,
                'correct': is_correct,
                'points_earned': question['points'] if is_correct else 0
            })

        # Calculate percentage
        percentage = (earned_points / total_points * 100) if total_points > 0 else 0
        passed = percentage >= quiz['pass_score']

        response_data = {
            'total_points': total_points,
            'earned_points': earned_points,
            'percentage': round(percentage, 2),
            'passed': passed,
            'results': results
        }

        return Response(response_data)

    # quiz attempts (without correct answers)
    @action(detail=True, methods=['get'])
    def attempt(self, request, pk=None):
        quiz = quizzes_collection.find_one({'_id': ObjectId(pk)})
        if not quiz:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Get questions and remove correct answers
        questions = list(questions_collection.find({'quiz_id': ObjectId(pk)}))
        for question in questions:
            if 'options' in question:
                if 'correct_answer' in question['options']:
                    del question['options']['correct_answer']
            if 'word_select_text' in question:
                if 'correct_words' in question['word_select_text']:
                    del question['word_select_text']['correct_words']
        
        quiz['questions'] = questions
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        quiz = quizzes_collection.find_one({'_id': ObjectId(pk)})
        if not quiz:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Delete all questions associated with this quiz
        questions_collection.delete_many({'quiz_id': ObjectId(pk)})
        # Delete the quiz itself
        quizzes_collection.delete_one({'_id': ObjectId(pk)})
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class QuestionViewSet(viewsets.ViewSet):
    """
    CRUD endpoints for Quiz:
    list: GET /api/questions/
    retrieve: GET /api/questions/{id}/
    create: POST /api/questions/
    delete: DELETE /api/questions/{id}/
    """
    def list(self, request):
        quiz_id = request.query_params.get('quiz_id')
        filter_params = {'quiz_id': ObjectId(quiz_id)} if quiz_id else {}
        questions = list(questions_collection.find(filter_params))
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        question = questions_collection.find_one({'_id': ObjectId(pk)})
        if not question:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def create(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question_id = Question.create_question(**serializer.validated_data)
            question = questions_collection.find_one({'_id': ObjectId(question_id)})
            return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        question = questions_collection.find_one({'_id': ObjectId(pk)})
        if not question:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        questions_collection.delete_one({'_id': ObjectId(pk)})
        return Response(status=status.HTTP_204_NO_CONTENT)
