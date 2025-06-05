#!/usr/bin/env python3
"""
Session authentication module for the API
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    SessionAuth class that inherits from Auth.
    This class handles session-based authentication mechanism.
    It manages session IDs and maps them to user IDs for authentication.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.

        Args:
            user_id (str): The user ID to create a session for

        Returns:
            str: The generated Session ID, or None if user_id is invalid

        The method validates the user_id parameter and generates a unique
        session ID using uuid4(). The session ID is stored as a key in the
        user_id_by_session_id dictionary with user_id as the value.
        """
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        # Generate a Session ID using uuid4()
        session_id = str(uuid.uuid4())

        # Store the session_id as key and user_id as value
        self.user_id_by_session_id[session_id] = user_id

        return session_id
