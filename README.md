# Quiz Application API

A RESTful API service for managing quizzes, user accounts, and quiz history.

Database: MongoDB
Hosting: AWS EC2

## Demo

Demo API Address: [http://3.1.84.199:8000](http://3.1.84.199:8000)

Demo website: [http://3.1.84.199:5173](http://3.1.84.199:5173)

## React Project

React prject address: [https://github.com/Jason9265/quiz-frontend](https://github.com/Jason9265/quiz-frontend)

## API Endpoints

### Authentication

#### Register User
- **URL:** `/api/auth/register/`
- **Method:** `POST`
- **Data:**
```json
{
    "username": "string",
    "password": "string"
}
```

#### Login
- **URL:** `/api/auth/login/`
- **Method:** `POST`
- **Data:**
```json
{
    "username": "string",
    "password": "string"
}
```

### Quiz Management

#### List All Quizzes
- **URL:** `/api/quizzes/`
- **Method:** `GET`

#### Get Quiz Details (Admin View)
- **URL:** `/api/quizzes/{quiz_id}/`
- **Method:** `GET`

#### Get Quiz for Attempt (Student View, without answers)
- **URL:** `/api/quizzes/{quiz_id}/attempt/`
- **Method:** `GET`

#### Submit Quiz(Check answers)
- **URL:** `/api/quizzes/{quiz_id}/submit/`
- **Method:** `POST`
- **Data:**
```json
{
    "answers": [
        {
            "question_id": "string",
            "answer": "string | array"
        }
    ]
}
```

#### Create Quiz
- **URL:** `/api/quizzes/`
- **Method:** `POST`
- **Data:**
```json
{
    "title": "string",
    "description": "string",
    "pass_score": "integer"
}
```

### Quiz History

#### Create Quiz History
- **URL:** `/api/auth/quiz-history/`
- **Method:** `POST`
- **Data:**
```json
{
    "user_name": "string",
    "quiz_id": "string",
    "total_points": "integer",
    "earned_points": "integer",
    "percentage": "float",
    "passed": "boolean",
    "results": [
        {
            "question_id": "string",
            "question_text": "string",
            "correct": "boolean",
            "points_earned": "integer",
            "submitted_answer": "string or array",
            "correct_answer": "string or array",
            "question_choices": ["string"]
        }
    ]
}
```

#### Get User's Quiz History
- **URL:** `/api/auth/quiz-history/user/{username}/`
- **Method:** `GET`

## Question Types

The system supports three types of questions:

### 1. Single Answer
- One correct answer from multiple choices
```json
{
    "question_type": "single",
    "options": {
        "choices": ["Option A", "Option B", "Option C"],
        "correct_answer": "Option A"
    }
}
```

### 2. Multiple Answer
- Multiple correct answers from choices
```json
{
    "question_type": "multiple",
    "options": {
        "choices": ["Option A", "Option B", "Option C"],
        "correct_answer": ["Option A", "Option B"]
    }
}
```

### 3. Word Select
- Select correct words from a sentence
```json
{
    "question_type": "word_select",
    "options": {
        "text": "Select the correct words in this sentence",
        "correct_answer": ["word1", "word2"]
    }
}
```

## Technical Stack

- AWS EC2
- Django REST Framework
- MongoDB
- Python 3.x

## Database Collections

- `users`: User account information
- `quizzes`: Quiz metadata and configuration
- `questions`: Quiz questions and answers
- `quiz_history`: Quiz attempt history and results
