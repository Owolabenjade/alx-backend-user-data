#!/usr/bin/env python3
"""
Session authentication views for the API
"""
from flask import request, jsonify, make_response, abort
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
        Response: JSON response with user data and session cookie, or error
                 message
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

    # Search for user by email - handle potential exceptions
    try:
        users = User.search({"email": email})
        if users is None:
            users = []
    except Exception as e:
        # If search fails, treat as no users found
        users = []

    # Check if user exists
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Validate password
    try:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
    except Exception as e:
        return jsonify({"error": "wrong password"}), 401

    # Import auth only when needed to avoid circular imports
    from api.v1.app import auth

    # Create session ID for the user
    session_id = auth.create_session(user.id)
    if session_id is None:
        return jsonify({"error": "failed to create session"}), 500

    # Create response with user data
    try:
        user_dict = user.to_json()
        response = make_response(jsonify(user_dict))
    except Exception as e:
        return jsonify({"error": "failed to serialize user"}), 500

    # Set session cookie
    cookie_name = getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(cookie_name, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    """
    Handles session authentication logout.

    This route processes DELETE requests to destroy user sessions and logout.
    It validates the session cookie, destroys the session, and returns an
    empty JSON response on success.

    Returns:
        Response: Empty JSON dictionary on success, or 404 if session
                 destruction fails
    """
    # Import auth only when needed to avoid circular imports
    from api.v1.app import auth

    # Attempt to destroy the session
    if not auth.destroy_session(request):
        # If destroy_session returns False, abort with 404
        abort(404)

    # Return empty JSON dictionary with status code 200
    return jsonify({}), 200
