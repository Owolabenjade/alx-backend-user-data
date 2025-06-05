#!/usr/bin/env python3
"""
Auth module for the API
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    Auth class to manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method that defines which paths don't need authentication

        Args:
            path (str): The requested path
            excluded_paths (List[str]): List of paths that don't require auth

        Returns:
            bool: True if path requires authentication, False otherwise
        """
        if path is None:
            return True

        if excluded_paths is None or excluded_paths == []:
            return True

        # Add trailing slash to path if it doesn't have one
        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            # Handle wildcard patterns
            if excluded_path.endswith('*'):
                # Remove the * and check if path starts with the prefix
                prefix = excluded_path[:-1]
                if path.startswith(prefix):
                    return False
            else:
                # Add trailing slash to excluded_path if it doesn't have one
                if excluded_path[-1] != '/':
                    excluded_path += '/'

                if path == excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Method that handles authorization header

        Args:
            request: Flask request object

        Returns:
            str: The authorization header value or None
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method that returns the current user

        Args:
            request: Flask request object

        Returns:
            User: The current user or None
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request.

        Args:
            request: Flask request object

        Returns:
            str: The value of the session cookie, or None if not found

        This method extracts the session cookie from the request using the
        cookie name defined by the SESSION_NAME environment variable.
        Returns None if the request is None or if the cookie is not found.
        """
        if request is None:
            return None

        # Get the cookie name from environment variable
        session_name = getenv('SESSION_NAME')

        # Use .get() to safely access the cookie from request.cookies
        return request.cookies.get(session_name)
