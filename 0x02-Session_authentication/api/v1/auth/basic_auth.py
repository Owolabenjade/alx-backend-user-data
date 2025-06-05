#!/usr/bin/env python3
"""
Basic authentication module for the API
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import base64


class BasicAuth(Auth):
    """BasicAuth class that inherits from Auth
    """
    
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization header
        
        Args:
            authorization_header: The Authorization header string
            
        Returns:
            The Base64 encoded string or None
        """
        if authorization_header is None:
            return None
            
        if not isinstance(authorization_header, str):
            return None
            
        if not authorization_header.startswith("Basic "):
            return None
            
        # Return everything after "Basic "
        return authorization_header[6:]
    
    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Decodes a Base64 string
        
        Args:
            base64_authorization_header: The Base64 string to decode
            
        Returns:
            The decoded string as UTF-8 or None
        """
        if base64_authorization_header is None:
            return None
            
        if not isinstance(base64_authorization_header, str):
            return None
            
        try:
            # Decode the base64 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            # Convert bytes to UTF-8 string
            return decoded_bytes.decode('utf-8')
        except Exception:
            # Return None for any decoding errors
            return None
    
    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Extracts user email and password from decoded Base64 string
        
        Args:
            decoded_base64_authorization_header: The decoded authorization string
            
        Returns:
            Tuple of (email, password) or (None, None)
        """
        if decoded_base64_authorization_header is None:
            return None, None
            
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
            
        if ':' not in decoded_base64_authorization_header:
            return None, None
            
        # Split on the first occurrence of ':'
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password
    
    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                      ) -> TypeVar('User'):
        """Returns a User instance based on email and password
        
        Args:
            user_email: The user's email
            user_pwd: The user's password
            
        Returns:
            User instance if credentials are valid, None otherwise
        """
        if user_email is None or not isinstance(user_email, str):
            return None
            
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
            
        # Search for users with the given email
        users = User.search({'email': user_email})
        
        # If no user found with this email
        if not users:
            return None
            
        # Check password for the first user found
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
            
        return user
    
    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request
        
        Args:
            request: The Flask request object
            
        Returns:
            User instance if authenticated, None otherwise
        """
        # Get the Authorization header
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
            
        # Extract the Base64 part
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None
            
        # Decode the Base64 string
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None
            
        # Extract user credentials
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if user_email is None or user_pwd is None:
            return None
            
        # Get and return the user object
        return self.user_object_from_credentials(user_email, user_pwd)