# Authentication APIs

Base URL: `http://127.0.0.1:5000`

## Post /auth/register

Registers a new user with hashed password.


### Request
```json
{
    "email": "admin@gmail.com",
    "password": "password123"
}
```

### Response
- 201 Created
- 400 User already exists


## Post /auth/login

Authenticates a user and returns a JWT token.

### Request
```json
{
    "email": "admin@gmail.com",
    "password": "password123"
}
```

### Response
```json
{
    "access_token": "<JWT_TOKEN>"
}
```

## GET /auth/me
Protected endpoint returning authenticated user details

### Header
```makefile
Authorization: Bearer <JWT_TOKEN>
```

### Response
```json
{
    "id": 1,
    "email": "admin@gmail.com",
    "created_at": "2025-12-23T13:45:10+00:00"
}
```
