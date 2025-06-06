#!/usr/bin/env python3
"""
UserSession module for database-backed session storage
"""
from models.base import Base


class UserSession(Base):
    """
    UserSession class that inherits from Base.
    This class represents a user session stored in the database,
    providing persistence for session data beyond application restarts.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a UserSession instance.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Initializes the UserSession with user_id and session_id attributes.
        Like the User class, it calls the parent Base class constructor
        and then sets up the specific attributes for session management.
        """
        super().__init__(*args, **kwargs)

        # Initialize session-specific attributes
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
