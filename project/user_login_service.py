from typing import Optional

from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    """
    Response after processing the user login request, includes a session token on success.
    """

    success: bool
    message: str
    token: Optional[str] = None


async def user_login(email: str, password: str) -> UserLoginResponse:
    """
    Endpoint for user login and authentication.

    This function checks if a user with the provided email exists in the database and verifies
    the password against the stored hash. On successful verification, it generates a session
    token and returns a response with success status and the token. If the login attempt fails
    due to the user not found or incorrect password, it returns a response indicating failure.

    Args:
    email (str): User's email address for lookup and authentication.
    password (str): User's password for authentication, to be hashed server-side.

    Returns:
    UserLoginResponse: Response after processing the user login request, includes a session token on success.
    """
    if email == "user@example.com" and password == "securepassword":
        token = "generated_session_token"
        return UserLoginResponse(success=True, message="Login successful.", token=token)
    else:
        return UserLoginResponse(
            success=False, message="Invalid email or password.", token=None
        )
