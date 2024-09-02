
# API Documentation

This document outlines the API endpoints available in the Django Admissions Tracker project.

## Authentication

All API endpoints require authentication. Use token-based authentication by including the token in the Authorization header:

```
Authorization: Token your_auth_token
```

To obtain a token, use the login endpoint.

## Endpoints

### Authentication

#### Login
- URL: `/api/auth/login/`
- Method: POST
- Data:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- Response:
  ```json
  {
    "token": "your_auth_token"
  }
  ```

### Admission Posts

#### List Posts
- URL: `/api/posts/`
- Method: GET
- Parameters:
  - `page`: Page number for pagination (default: 1)
  - `sort`: Sort field (options: created_at, -created_at, university, status)
- Response:
  ```json
  {
    "count": 100,
    "next": "http://example.com/api/posts/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "user": "username",
        "degree_type": "MS",
        "major": "Computer Science",
        "university": "Example University",
        "status": "APPLIED",
        "created_at": "2023-05-01T12:00:00Z"
      },
      ...
    ]
  }
  ```

#### Create Post
- URL: `/api/posts/`
- Method: POST
- Data:
  ```json
  {
    "degree_type": "MS",
    "major": "Computer Science",
    "university": "Example University",
    "country": "USA",
    "application_round": "Fall 2024",
    "status": "APPLIED",
    "gpa": 3.8,
    "test_type": "GRE",
    "test_score": 320,
    "student_type": "INTERNATIONAL"
  }
  ```
- Response: Created post object

#### Retrieve Post
- URL: `/api/posts/{id}/`
- Method: GET
- Response: Detailed post object

#### Update Post
- URL: `/api/posts/{id}/`
- Method: PUT
- Data: Updated post fields
- Response: Updated post object

#### Delete Post
- URL: `/api/posts/{id}/`
- Method: DELETE
- Response: 204 No Content

### Comments

#### List Comments for a Post
- URL: `/api/posts/{post_id}/comments/`
- Method: GET
- Response: List of comments for the specified post

#### Add Comment
- URL: `/api/posts/{post_id}/comments/`
- Method: POST
- Data:
  ```json
  {
    "content": "Your comment text here"
  }
  ```
- Response: Created comment object

#### Delete Comment
- URL: `/api/comments/{comment_id}/`
- Method: DELETE
- Response: 204 No Content

### Likes

#### Like/Unlike Post
- URL: `/api/posts/{post_id}/like/`
- Method: POST
- Response:
  ```json
  {
    "liked": true,
    "likes_count": 42
  }
  ```

## Error Handling

All endpoints return appropriate HTTP status codes:

- 200: Successful GET, PUT, PATCH requests
- 201: Successful POST requests
- 204: Successful DELETE requests
- 400: Bad request (invalid data)
- 401: Unauthorized (invalid or missing token)
- 403: Forbidden (insufficient permissions)
- 404: Not found
- 500: Internal server error

Error responses include a message explaining the error.