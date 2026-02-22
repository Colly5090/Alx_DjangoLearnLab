# Authentication and Permission Setup Documentation

## Overview

This project uses **Django REST Framework (DRF)** with **Token-based Authentication** and **permission classes** to secure API endpoints.  
Authentication ensures that only verified users can access the API, while permissions control **what actions each authenticated user is allowed to perform**.

This setup is suitable for APIs that require user-based access control without relying on session authentication.

---

## Authentication Configuration

### Authentication Method Used
- **DRF Token Authentication**

Each authenticated user is assigned a unique token stored in the database.  
Clients must include this token in the `Authorization` header for every protected request.

### Installed App

In `settings.py`, token authentication is enabled by adding:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
]

python manage.py migrate
```

In `settings.py`, the default authentication class is configured:

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

### Token Generation and Usage
```python
from rest_framework.authtoken.views import obtain_auth_token

# Example urls.py configuration
path('token/', obtain_auth_token, name='api-token')
```

#### Request Example (Token Creation)
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
-H "Content-Type: application/json" \
-d '{"username":"user1","password":"password123"}'
```

#### Response Example
```json
{
  "token": "a1b2c3d4e5f6..."
}
```

#### Using the Token in Requests
The token must be included in the `Authorization` header for all protected endpoints:
```http
Authorization: Token a1b2c3d4e5f6...
```


