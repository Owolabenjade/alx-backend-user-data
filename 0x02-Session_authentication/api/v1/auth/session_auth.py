#!/usr/bin/env python3
"""
Session authentication module for the API
"""
from api.v1.auth.auth import Auth
from models.user import User
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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID.

        Args:
            session_id (str): The session ID to look up

        Returns:
            str: The user ID associated with the session ID,
            or None if not found

        The method validates the session_id parameter
        and uses the get() method to safely retrieve the
        user_id from the user_id_by_session_id dictionary.
        Returns None if session_id is invalid or
        not found in the dictionary.
        """
        if session_id is None:
            return None

        if not isinstance(session_id, str):
            return None

        # Use .get() to safely access the dictionary
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value.

        Args:
            request: Flask request object

        Returns:
            User: User instance if found, None otherwise

        This method overloads the current_user method from Auth class.
        It uses session_cookie() to extract the session ID from the request
        cookie, then uses user_id_for_session_id() to get the user ID,
        and finally retrieves the User instance from the database.
        """
        try:
            # Get the session ID from the cookie
            session_id = self.session_cookie(request)

            if session_id is None:
                return None

            # Get the user ID based on the session ID
            user_id = self.user_id_for_session_id(session_id)

            if user_id is None:
                return None

            # Retrieve and return the User instance from the database
            user = User.get(user_id)
            return user

        except Exception:
            # Return None if any exception occurs during user retrieval
            return None
