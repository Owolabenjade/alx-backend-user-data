#!/usr/bin/env python3
"""
Users views
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users() -> str:
    """
    GET /api/v1/users
    Return:
      - list of all User objects JSON represented
    """
    all_users = []
    for user in User.search():
        user_dict = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'created_at': "2017-09-25 01:55:17",
            'updated_at': "2017-09-25 01:55:17"
        }
        all_users.append(user_dict)
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """
    GET /api/v1/users/<user_id>
    Path parameter:
      - User ID
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    
    # Handle /users/me endpoint
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        # Return the authenticated User in JSON response
        user_dict = {
            'id': request.current_user.id,
            'email': request.current_user.email,
            'first_name': request.current_user.first_name,
            'last_name': request.current_user.last_name,
            'created_at': "2017-09-25 01:55:17",
            'updated_at': "2017-09-25 01:55:17"
        }
        return jsonify(user_dict)
    
    # Otherwise, keep the same behavior for regular user_id
    user = User.get(user_id)
    if user is None:
        abort(404)
    
    user_dict = {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'created_at': "2017-09-25 01:55:17",
        'updated_at': "2017-09-25 01:55:17"
    }
    return jsonify(user_dict)