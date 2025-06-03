#!/usr/bin/env python3
"""
Authentication module.
"""
import bcrypt
import uuid
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hash a password with bcrypt.
    
    Args:
        password (str): Password to hash
        
    Returns:
        bytes: Salted hash of the password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """
    Generate a new UUID.
    
    Returns:
        str: String representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initialize Auth instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.
        
        Args:
            email (str): User's email
            password (str): User's password
            
        Returns:
            User: The created user object
            
        Raises:
            ValueError: If user already exists
        """
        try:
            # Check if user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User doesn't exist, create new one
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password.decode('utf-8'))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user login credentials.
        
        Args:
            email (str): User's email
            password (str): User's password
            
        Returns:
            bool: True if credentials are valid, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), 
                                user.hashed_password.encode('utf-8'))
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """
        Create a session for a user.
        
        Args:
            email (str): User's email
            
        Returns:
            str or None: Session ID if user exists, None otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Get user from session ID.
        
        Args:
            session_id (str): Session ID
            
        Returns:
            User or None: User object if found, None otherwise
        """
        if session_id is None:
            return None
        
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a user's session.
        
        Args:
            user_id (int): User's ID
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset password token for a user.
        
        Args:
            email (str): User's email
            
        Returns:
            str: Reset token
            
        Raises:
            ValueError: If user does not exist
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError(f"User with email {email} does not exist")

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update user's password using reset token.
        
        Args:
            reset_token (str): Reset token
            password (str): New password
            
        Raises:
            ValueError: If reset token is invalid
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, 
                               hashed_password=hashed_password.decode('utf-8'),
                               reset_token=None)
        except NoResultFound:
            raise ValueError("Invalid reset token")