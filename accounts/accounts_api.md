# Accounts API Documentation

## Base URL
`http://localhost:8000/api/auth/`

## Authentication Endpoints

### Register New User
- **URL:** `/register/`
- **Method:** `POST`
- **Description:** Create a new user account
- **Data Parameters:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Success Response:**
  - **Code:** 201 CREATED
  ```json
  {
    "id": "string",
    "username": "string",
    "message": "User created successfully"
  }
  ```
- **Error Response:**
  - **Code:** 400 BAD REQUEST
  ```json
  {
    "error": "Username already exists"
  }
  ```
  OR
  ```json
  {
    "username": ["This field is required."],
    "password": ["This field is required."]
  }
  ```

### User Login
- **URL:** `/login/`
- **Method:** `POST`
- **Description:** Authenticate user and get access
- **Data Parameters:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Success Response:**
  - **Code:** 200 OK
  ```json
  {
    "id": "string",
    "username": "string",
    "message": "Login successful"
  }
  ```
- **Error Response:**
  - **Code:** 401 UNAUTHORIZED
  ```json
  {
    "error": "Invalid credentials"
  }
  ```

## Data Models

### User Model
```json
{
    "_id": "ObjectId",
    "username": "string",
    "password": "string",
    "created_at": "datetime"
}
```

## Example Requests

### Register Example
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure123"
  }'
```

### Login Example
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure123"
  }'
```

## Notes
1. All requests must include `Content-Type: application/json` header
2. Passwords are currently stored as plain text (not recommended for production)
3. No token-based authentication is implemented yet
4. Username must be unique in the system