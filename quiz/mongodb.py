from pymongo import MongoClient
from bson import ObjectId
import json
from django.conf import settings

# Check if we're running tests
import sys
TESTING = 'test' in sys.argv

# Use test database if running tests
DB_NAME = 'quiz_app_test' if TESTING else 'quiz_app'

client = MongoClient("mongodb+srv://remote-user:uijNe16U2k2Si4Fk@cluster0.ruula.mongodb.net/quiz_app?retryWrites=true&w=majority")
db = client[DB_NAME]

quizzes_collection = db['quizzes']
questions_collection = db['questions']

def serialize_mongo_id(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")