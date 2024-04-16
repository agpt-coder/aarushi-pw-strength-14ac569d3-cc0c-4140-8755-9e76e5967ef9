import prisma
import prisma.models
from pydantic import BaseModel


class PasswordResetResponse(BaseModel):
    """
    This model communicates the result of a password reset request initiation, indicating whether the request was successfully received and processed.
    """

    status: str
    message: str


async def password_reset(email: str) -> PasswordResetResponse:
    """
    Endpoint for users to reset their password.

    Args:
    email (str): The email address associated with the user account for which the password reset is requested.

    Returns:
    PasswordResetResponse: This model communicates the result of a password reset request initiation, indicating whether the request was successfully received and processed.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user:
        return PasswordResetResponse(
            status="Error",
            message="If this email is registered, you will receive a password reset link.",
        )
    return PasswordResetResponse(
        status="Success",
        message="A password reset link has been sent to your email address if it exists in our system.",
    )
