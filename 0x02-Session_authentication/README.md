# 0x02. Session Authentication

This project implements Session Authentication for a REST API.

## Learning Objectives

- What authentication means
- What session authentication means
- What Cookies are
- How to send Cookies
- How to parse Cookies

## Files

- `api/v1/app.py` - Main Flask application
- `api/v1/views/users.py` - User endpoints
- `models/` - Data models
- `api/v1/auth/` - Authentication classes

## Usage

```bash
API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app