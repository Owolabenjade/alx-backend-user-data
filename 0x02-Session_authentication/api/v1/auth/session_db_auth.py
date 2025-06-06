#!/usr/bin/env python3
"""
Session database authentication module for the API
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class that inherits from SessionExpAuth.
    This class implements database-backed session storage, providing
    persistence for sessions across application restarts. Sessions are
    stored as UserSession instances in the database rather than in memory.
    """

    def create_session(self, user_id=None):
        """
        Creates and stores a new instance of UserSession and returns
        the Session ID.

        Args:
            user_id (str): The user ID to create a session for

        Returns:
            str: The generated Session ID, or None if creation fails

        This method overloads the create_session method from SessionExpAuth.
        Instead of storing session data in memory, it creates a UserSession
        instance in the database for persistence.
        """
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        # Generate a Session ID using the parent class method
        # This will create the session ID but store it in memory
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        # Create a new UserSession instance
        user_session = UserSession()
        user_session.user_id = user_id
        user_session.session_id = session_id

        # Save the UserSession to the database
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID by requesting UserSession in the database
        based on session_id.

        Args:
            session_id (str): The session ID to look up

        Returns:
            str: The user ID if session is valid
            and not expired, None otherwise

        This method overloads the user_id_for_session_id method from
        SessionExpAuth. It retrieves session data from the database
        and applies expiration logic based on the session's creation time.
        """
        if session_id is None:
            return None

        try:
            # Search for UserSession by session_id
            user_sessions = UserSession.search({'session_id': session_id})

            if not user_sessions or len(user_sessions) == 0:
                return None

            user_session = user_sessions[0]

            # If session_duration is 0 or negative, no expiration
            if self.session_duration <= 0:
                return user_session.user_id

            # Check if session has expired
            created_at = user_session.created_at

            # Calculate expiration time
            expiration_time = (created_at +
                               timedelta(seconds=self.session_duration))

            # Return None if session has expired
            if expiration_time < datetime.now():
                return None

            # Session is still valid, return the user_id
            return user_session.user_id

        except Exception:
            # Return None if any exception occurs during retrieval
            return None

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on
        the Session ID from the request cookie.

        Args:
            request: Flask request object

        Returns:
            bool: True if session was successfully destroyed, False otherwise

        This method overloads the destroy_session method from SessionExpAuth.
        It removes the UserSession instance from the database rather than
        just removing it from memory.
        """
        if request is None:
            return False

        # Get the session ID from the cookie
        session_id = self.session_cookie(request)

        if session_id is None:
            return False

        try:
            # Search for UserSession by session_id
            user_sessions = UserSession.search({'session_id': session_id})

            if not user_sessions or len(user_sessions) == 0:
                return False

            user_session = user_sessions[0]

            # Remove the UserSession from the database
            user_session.remove()

            return True

        except Exception:
            # Return False if any exception occurs during removal
            return False
