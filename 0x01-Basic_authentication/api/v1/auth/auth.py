#!/usr/bin/env python3
"""
Auth module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required for a given path
        
        Args:
            path: The path to check
            excluded_paths: List of paths that don't require authentication
            
        Returns:
            True if path requires authentication, False otherwise
        """
        if path is None:
            return True
            
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
            
        # Ensure path ends with / for consistent comparison
        if not path.endswith('/'):
            path = path + '/'
            
        # Check if path is in excluded_paths
        for excluded_path in excluded_paths:
            if path == excluded_path:
                return False
                
        return True

    def authorization_header(self, request=None) -> str:
        """Gets the authorization header from the request
        
        Args:
            request: The Flask request object
            
        Returns:
            The value of the Authorization header or None
        """
        if request is None:
            return None
            
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user from the request
        
        Args:
            request: The Flask request object
            
        Returns:
            None - for now, will be implemented later
        """
        return None
