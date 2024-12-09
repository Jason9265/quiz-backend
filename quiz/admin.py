from django.contrib import admin
from .models import Quiz, Question

# For admin panel, can be used to add quizzes and questions later
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'pass_score')
    search_fields = ('title', 'description')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz_id', 'question_type', 'text', 'points')
    list_filter = ('quiz_id', 'question_type')