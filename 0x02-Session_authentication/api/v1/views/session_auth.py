#!/usr/bin/env python3
"""
Session authentication views for the API
"""
from flask import request, jsonify, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    Handles session authentication login.
    
    This route processes POST requests to authenticate users and create
    session cookies. It validates email and password, creates a session ID,
    and sets the session cookie in the response.
    
    Returns:
        Response: JSON response with user data and session cookie, or error message
    """
    # Get email and password from form data
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Validate email parameter
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    
    # Validate password parameter
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    
    # Search for user by email
    users = User.search({"email": email})
    
    # Check if user exists
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    
    user = users[0]
    
    # Validate password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    
    # Import auth only when needed to avoid circular imports
    from api.v1.app import auth
    
    # Create session ID for the user
    session_id = auth.create_session(user.id)
    
    # Create response with user data
    response = make_response(jsonify(user.to_json()))
    
    # Set session cookie
    cookie_name = getenv('SESSION_NAME')
    response.set_cookie(cookie_name, session_id)
    
    return response