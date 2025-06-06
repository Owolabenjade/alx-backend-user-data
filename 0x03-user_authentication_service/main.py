#!/usr/bin/env python3
"""
End-to-end integration test module for user authentication service.

This module contains test functions that interact with a Flask web server
to validate user authentication functionality including registration,
login, logout, profile access, and password reset operations.
"""

import requests


def register_user(email: str, password: str) -> None:
    """
    Register a new user with the authentication service.

    Args:
        email (str): The user's email address
        password (str): The user's password

    Raises:
        AssertionError: If the registration
        fails or returns unexpected response
    """
    url = "http://localhost:5000/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)

    assert response.status_code == 200
    expected_payload = {"email": email, "message": "user created"}
    assert response.json() == expected_payload


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test login with incorrect password to verify authentication fails.

    Args:
        email (str): The user's email address
        password (str): An incorrect password

    Raises:
        AssertionError: If login succeeds with wrong password
    """
    url = "http://localhost:5000/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Log in a user with correct credentials and return session ID.

    Args:
        email (str): The user's email address
        password (str): The user's correct password

    Returns:
        str: The session ID from the response cookies

    Raises:
        AssertionError: If login fails or returns unexpected response
    """
    url = "http://localhost:5000/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)

    assert response.status_code == 200
    expected_payload = {"email": email, "message": "logged in"}
    assert response.json() == expected_payload

    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    Test accessing profile endpoint without authentication.

    Raises:
        AssertionError: If profile access succeeds without authentication
    """
    url = "http://localhost:5000/profile"
    response = requests.get(url)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Test accessing profile endpoint with valid session.

    Args:
        session_id (str): Valid session ID from login

    Raises:
        AssertionError: If profile access fails with valid session
    """
    url = "http://localhost:5000/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)

    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """
    Log out a user using their session ID.

    Args:
        session_id (str): Valid session ID to log out

    Raises:
        AssertionError: If logout fails or returns unexpected response
    """
    url = "http://localhost:5000/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)

    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Request a password reset token for the given email.

    Args:
        email (str): The user's email address

    Returns:
        str: The reset token from the response

    Raises:
        AssertionError: If reset token request fails
    """
    url = "http://localhost:5000/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)

    assert response.status_code == 200
    response_json = response.json()
    assert "email" in response_json
    assert "reset_token" in response_json
    assert response_json["email"] == email

    return response_json["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update user password using reset token.

    Args:
        email (str): The user's email address
        reset_token (str): Valid reset token
        new_password (str): The new password to set

    Raises:
        AssertionError: If password update fails or returns unexpected response
    """
    url = "http://localhost:5000/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(url, data=data)

    assert response.status_code == 200
    expected_payload = {"email": email, "message": "Password updated"}
    assert response.json() == expected_payload


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
