from django.db import models
from datetime import datetime

# Create your models here.

class User:
    @staticmethod
    def create_user(username, password):
        from .mongodb import users_collection
        # Check if username exists
        if users_collection.find_one({'username': username}):
            return None
        
        user_data = {
            'username': username,
            'password': password,
            'created_at': datetime.now()
        }
        result = users_collection.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    def get_user(username):
        from .mongodb import users_collection
        return users_collection.find_one({'username': username})

class QuizHistory:
    @staticmethod
    def create_history(user_name, quiz_id, total_points, earned_points, percentage, passed, results, title=None, quiz_time=None):
        from .mongodb import quiz_history_collection
        from datetime import datetime
        
        history_data = {
            'user_name': user_name,
            'quiz_id': quiz_id,
            'total_points': total_points,
            'earned_points': earned_points,
            'percentage': percentage,
            'passed': passed,
            'results': results,
            'title': title,
            'quiz_time': quiz_time if quiz_time else datetime.utcnow()
        }
        
        result = quiz_history_collection.insert_one(history_data)
        return str(result.inserted_id)

    @staticmethod
    def get_user_history(user_name):
        from .mongodb import quiz_history_collection
        return list(quiz_history_collection.find({'user_name': user_name}))

    # get quiz history by quiz_id & user_name
    @staticmethod
    def get_quiz_history(quiz_id, user_name):
        from .mongodb import quiz_history_collection
        return list(quiz_history_collection.find({'quiz_id': quiz_id, 'user_name': user_name}))
