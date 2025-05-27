#!/usr/bin/env python3
"""
User module
"""
import hashlib
import uuid
from typing import List


class User:
    """User class
    """
    
    # Class variable to store all users (simulating a database)
    _users = []
    
    def __init__(self):
        """Initialize a User instance
        """
        self.id = str(uuid.uuid4())
        self.email = None
        self.password = None
        self.first_name = None
        self.last_name = None
        
    @property
    def password(self):
        """Getter for password
        """
        return self._password
        
    @password.setter
    def password(self, pwd):
        """Setter for password - stores hashed password
        """
        if pwd is None or not isinstance(pwd, str):
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest()
            
    def is_valid_password(self, pwd: str) -> bool:
        """Validates a password
        
        Args:
            pwd: The password to validate
            
        Returns:
            True if password is valid, False otherwise
        """
        if pwd is None or not isinstance(pwd, str):
            return False
        if self.password is None:
            return False
        return hashlib.sha256(pwd.encode()).hexdigest() == self.password
        
    def display_name(self) -> str:
        """Display User name based on email/first_name/last_name
        """
        if self.email is None and self.first_name is None and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        return "{} {}".format(self.first_name, self.last_name)
        
    def save(self):
        """Save the user to the database (class variable)
        """
        # Remove existing user with same id if any
        User._users = [u for u in User._users if u.id != self.id]
        # Add this user
        User._users.append(self)
        
    @classmethod
    def search(cls, attributes: dict = {}) -> List["User"]:
        """Search users with matching attributes
        
        Args:
            attributes: Dictionary of attributes to match
            
        Returns:
            List of User instances that match all attributes
        """
        if not attributes:
            return cls._users
            
        matching_users = []
        for user in cls._users:
            match = True
            for key, value in attributes.items():
                if not hasattr(user, key) or getattr(user, key) != value:
                    match = False
                    break
            if match:
                matching_users.append(user)
        return matching_users