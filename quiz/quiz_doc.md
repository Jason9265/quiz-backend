# Quiz API Documentation

## Base URL
`http://3.1.84.199:8000/api/`

## Quizzes Endpoints

### List All Quizzes
- **URL:** `/quizzes/`
- **Method:** `GET`
- **Success Response:**
  ```json
  [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "pass_score": "integer",
    }
  ]
  ```

### Get Quiz (Admin View)
- **URL:** `/quizzes/{quiz_id}/`
- **Method:** `GET`
- **URL Parameters:** `quiz_id=[string]`
- **Description:** Returns quiz with correct answers (for admin use)
- **Success Response:**
  ```json
  {
    "id": "string",
    "title": "string",
    "description": "string",
    "pass_score": "integer",
    "questions": [
      {
        "id": "string",
        "quiz_id": "string",
        "question_type": "string",
        "text": "string",
        "points": "integer",
        "options": {
          "choices": ["string"],
          "correct_answer": "string or array"
        }
      }
    ]
  }
  ```

### Get Quiz Attempt (Student View)
- **URL:** `/quizzes/{quiz_id}/attempt/`
- **Method:** `GET`
- **URL Parameters:** `quiz_id=[string]`
- **Description:** Returns quiz without correct answers (for student attempts)
- **Success Response:**
  ```json
  {
    "id": "string",
    "title": "string",
    "description": "string",
    "pass_score": "integer",
    "questions": [
      {
        "id": "string",
        "quiz_id": "string",
        "question_type": "string",
        "text": "string",
        "points": "integer",
        "options": {
          "choices": ["string"]
        }
      }
    ]
  }
  ```

### Submit Quiz Answers
- **URL:** `/quizzes/{quiz_id}/submit/`
- **Method:** `POST`
- **URL Parameters:** `quiz_id=[string]`
- **Data Parameters:**
  ```json
  {
    "answers": [
      {
        "question_id": "string",
        "answer": "string or array"
      }
    ]
  }
  ```
- **Success Response:**
  ```json
  {
    "total_points": "integer",
    "earned_points": "integer",
    "percentage": "float",
    "passed": "boolean",
    "results": [
      {
        "question_id": "string",
        "correct": "boolean",
        "points_earned": "integer"
      }
    ]
  }
  ```

### Create Quiz
- **URL:** `/quizzes/`
- **Method:** `POST`
- **Data Parameters:**
  ```json
  {
    "title": "string",
    "description": "string",
    "pass_score": "integer"
  }
  ```
- **Success Response:**
  - **Code:** 201 CREATED
  ```json
  {
    "id": "string",
    "title": "string",
    "description": "string",
    "pass_score": "integer"
  }
  ```

## Question Types

### Single Answer
```json
{
  "question_type": "single",
  "options": {
    "choices": ["Option A", "Option B", "Option C"],
    "correct_answer": "Option A"
  }
}
```

### Multiple Answer
```json
{
  "question_type": "multiple",
  "options": {
    "choices": ["Option A", "Option B", "Option C"],
    "correct_answer": ["Option A", "Option B"]
  }
}
```

### Word Select
```json
{
  "question_type": "word_select"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Error message describing the issue"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```