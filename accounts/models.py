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
