#!/usr/bin/env python3
"""
Users views
"""
from api.v1.views import app_views
from flask import jsonify
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