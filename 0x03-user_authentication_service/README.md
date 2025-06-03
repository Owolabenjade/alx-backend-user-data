# User Authentication Service

A complete Flask-based authentication service implementing user registration, login, session management, and password reset functionality.

## Features

- User registration with email and password
- Secure password hashing using bcrypt
- Session-based authentication
- Password reset functionality
- SQLAlchemy database integration
- RESTful API endpoints

## Project Structure

```
0x03-user_authentication_service/
├── user.py              # SQLAlchemy User model
├── db.py                # Database operations
├── auth.py              # Authentication logic
├── app.py               # Flask application
└── README.md            # This file
```

## Requirements

- Python 3.7+
- Flask
- SQLAlchemy 1.3.x
- bcrypt

## Installation

```bash
pip3 install bcrypt flask sqlalchemy
```

## API Endpoints

### GET /
Returns a welcome message.

**Response:**
```json
{"message": "Bienvenue"}
```

### POST /users
Register a new user.

**Parameters:**
- `email` (form data): User's email
- `password` (form data): User's password

**Response:**
- Success (200): `{"email": "<email>", "message": "user created"}`
- Error (400): `{"message": "email already registered"}`

### POST /sessions
Log in a user.

**Parameters:**
- `email` (form data): User's email
- `password` (form data): User's password

**Response:**
- Success (200): `{"email": "<email>", "message": "logged in"}` + session cookie
- Error (401): Unauthorized

### DELETE /sessions
Log out a user.

**Parameters:**
- `session_id` (cookie): User's session ID

**Response:**
- Success: Redirect to /
- Error (403): Forbidden

### GET /profile
Get user profile.

**Parameters:**
- `session_id` (cookie): User's session ID

**Response:**
- Success (200): `{"email": "<email>"}`
- Error (403): Forbidden

### POST /reset_password
Generate password reset token.

**Parameters:**
- `email` (form data): User's email

**Response:**
- Success (200): `{"email": "<email>", "reset_token": "<token>"}`
- Error (403): Forbidden

### PUT /reset_password
Update password using reset token.

**Parameters:**
- `email` (form data): User's email
- `reset_token` (form data): Reset token
- `new_password` (form data): New password

**Response:**
- Success (200): `{"email": "<email>", "message": "Password updated"}`
- Error (403): Forbidden

## Usage

1. Start the Flask application:
```bash
python3 app.py
```

2. The server will run on `http://0.0.0.0:5000`

3. Use curl or any HTTP client to interact with the API:
```bash
# Register a user
curl -XPOST localhost:5000/users -d 'email=test@test.com' -d 'password=password123'

# Log in
curl -XPOST localhost:5000/sessions -d 'email=test@test.com' -d 'password=password123' -v

# Get profile (use session_id from login response)
curl -XGET localhost:5000/profile -b "session_id=<session_id>"
```

## Database

The application uses SQLite database (`a.db`) with the following User model:

- `id`: Integer primary key
- `email`: Non-nullable string (250 chars)
- `hashed_password`: Non-nullable string (250 chars)
- `session_id`: Nullable string (250 chars)
- `reset_token`: Nullable string (250 chars)

## Security Features

- Passwords are hashed using bcrypt with salt
- Session-based authentication using UUIDs
- Password reset tokens are time-limited UUIDs
- Input validation and proper error handling
- No direct database access from Flask app (uses Auth class)

## Code Style

The project follows:
- PEP 8 style guidelines (pycodestyle)
- Type annotations for all functions
- Comprehensive docstrings for all modules, classes, and functions
- Proper error handling and validation