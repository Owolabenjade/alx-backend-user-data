#!/usr/bin/env python3
"""
Session expiration authentication module for the API
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class that inherits from SessionAuth.
    This class adds session expiration functionality to the basic
    session authentication mechanism. Sessions automatically expire
    after a configurable duration.
    """

    def __init__(self):
        """
        Initialize the SessionExpAuth instance.

        Sets up the session_duration attribute from the SESSION_DURATION
        environment variable. If the environment variable doesn't exist
        or can't be parsed to an integer, assigns 0 (no expiration).
        """
        super().__init__()

        try:
            # Get SESSION_DURATION from environment and cast to int
            session_duration = getenv('SESSION_DURATION')
            self.session_duration = int(session_duration)
        except (TypeError, ValueError):
            # If SESSION_DURATION doesn't exist or can't be parsed to int
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a Session ID with expiration data for a user_id.

        Args:
            user_id (str): The user ID to create a session for

        Returns:
            str: The generated Session ID, or None if creation fails

        This method overloads the create_session method from SessionAuth.
        It creates a session ID using the parent class method, then stores
        additional metadata including the creation timestamp for expiration
        tracking.
        """
        # Create a Session ID by calling the parent class method
        session_id = super().create_session(user_id)

        # Return None if super() couldn't create a Session ID
        if session_id is None:
            return None

        # Create session dictionary with user_id and creation timestamp
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        # Store the session dictionary using session_id as key
        self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns a User ID based on a Session ID with expiration checking.

        Args:
            session_id (str): The session ID to look up

        Returns:
            str: The user ID if session is valid
            and not expired, None otherwise

        This method overloads the user_id_for_session_id
        method from SessionAuth.
        It adds expiration logic to validate that sessions haven't exceeded
        their configured duration.
        """
        # Return None if session_id is None
        if session_id is None:
            return None

        # Return None if session_id doesn't exist in the dictionary
        if session_id not in self.user_id_by_session_id:
            return None

        # Get the session dictionary
        session_dict = self.user_id_by_session_id[session_id]

        # Return user_id if session_duration is 0 or negative (no expiration)
        if self.session_duration <= 0:
            return session_dict.get('user_id')

        # Return None if session dictionary doesn't contain created_at
        if 'created_at' not in session_dict:
            return None

        # Get the creation time
        created_at = session_dict['created_at']

        # Calculate expiration time
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        # Return None if session has expired
        if expiration_time < datetime.now():
            return None

        # Session is still valid, return the user_id
        return session_dict.get('user_id')
