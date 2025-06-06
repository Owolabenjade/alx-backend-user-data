#!/usr/bin/env python3
"""
User model for authentication service.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model for users table.

    Attributes:
        id (int): Primary key, auto-incrementing integer
        email (str): Non-nullable string for user email
        hashed_password (str): Non-nullable string for hashed password
        session_id (str): Nullable string for session identification
        reset_token (str): Nullable string for password reset token
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
