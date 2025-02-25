# API Reference Guide

This document provides a reference for the authentication APIs in the **Crib Hunt Backend**. It includes request payloads, expected responses, and error handling for each endpoint.

## Base URL
```
http://127.0.0.1:8000/auth/
```

## Endpoints

### 1. User Registration
**Endpoint:**
```
POST /auth/register/
```

**Request Payload:**
```json
{
    "email": "user@example.com",
    "username": "user123",
    "password": "securepassword",
    "phone_number": "0712345678",
    "is_landlord": false,
    "is_renter": true
}
```

**Success Response:**
```json
{
    "message": "User registered successfully!"
}
```

**Error Response (Validation Error):**
```json
{
    "errors": {
        "email": ["This field must be unique."],
        "password": ["Ensure this field has at least 6 characters."]
    }
}
```

---

### 2. User Login
**Endpoint:**
```
POST /auth/login/
```

**Request Payload:**
```json
{
    "email": "user@example.com",
    "password": "securepassword"
}
```

**Success Response:**
```json
{
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}
```

**Error Response (Invalid Credentials):**
```json
{
    "error": "Incorrect password."
}
```

**Error Response (User Not Found):**
```json
{
    "error": "User with this email does not exist."
}
```

---

### 3. Get User Profile
**Endpoint:**
```
GET /auth/profile/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response:**
```json
{
    "id": 1,
    "email": "user@example.com",
    "username": "user123",
    "phone_number": "0712345678",
    "profile_picture": "http://127.0.0.1:8000/media/profile_pics/image.jpg",
    "is_landlord": false,
    "is_renter": true
}
```

**Error Response (Invalid Token):**
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid"
}
```

---

### 4. Refresh Access Token
**Endpoint:**
```
POST /auth/token/refresh/
```

**Request Payload:**
```json
{
    "refresh": "<refresh_token>"
}
```

**Success Response:**
```json
{
    "access": "<new_access_token>"
}
```

**Error Response (Invalid Refresh Token):**
```json
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```

---

### 5. Logout (Blacklist Refresh Token)
**Endpoint:**
```
POST /auth/logout/
```

**Request Payload:**
```json
{
    "refresh": "<refresh_token>"
}
```

**Success Response:**
```json
{
    "message": "Logout successful."
}
```

**Error Response (Invalid Token):**
```json
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```

---

## Notes
- **Authorization**: Most endpoints require an `Authorization: Bearer <access_token>` header.
- **Token Expiry**: Access tokens expire quickly; use the refresh token to get a new access token when needed.
- **Password Hashing**: Passwords are stored securely using Django's built-in hashing mechanism.

---

### Status Codes
| Status Code | Description |
|-------------|-------------|
| 200 OK | Request successful |
| 201 Created | User successfully registered |
| 400 Bad Request | Invalid input data |
| 401 Unauthorized | Invalid credentials or token |
| 404 Not Found | Resource not found |
| 500 Internal Server Error | Server-side error |

---

This document serves as a reference for frontend integration. Ensure the API base URL matches the deployment environment before making requests.