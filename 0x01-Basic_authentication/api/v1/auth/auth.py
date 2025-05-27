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
            False - for now, will be implemented later
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Gets the authorization header from the request
        
        Args:
            request: The Flask request object
            
        Returns:
            None - for now, will be implemented later
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user from the request
        
        Args:
            request: The Flask request object
            
        Returns:
            None - for now, will be implemented later
        """
        return None
