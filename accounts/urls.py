from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('quiz-history/', views.create_quiz_history, name='create-quiz-history'),
    path('quiz-history/user/<str:username>/', views.get_user_quiz_history, name='user-quiz-history'),
    path('quiz-history/quiz/<str:quiz_id>/', views.get_quiz_history, name='quiz-history'),
] 