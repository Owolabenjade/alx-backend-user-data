#!/usr/bin/env python3
"""
Basic authentication module for the API
"""
from api.v1.auth.auth import Auth
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