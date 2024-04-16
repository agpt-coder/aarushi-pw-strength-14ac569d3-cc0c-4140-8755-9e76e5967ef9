from typing import Optional

import prisma
import prisma.enums
import prisma.models
from passlib.hash import bcrypt
from pydantic import BaseModel


class UserRegistrationResponse(BaseModel):
    """
    A simple model to confirm successful registration or provide error messages. This model can be extended to include user ID or initial profile settings.
    """

    success: bool
    message: str
    user_id: Optional[str] = None


async def register_user(
    email: str, password: str, username: str
) -> UserRegistrationResponse:
    """
    Endpoint to register a new user.

    Args:
        email (str): The email address of the new user. Must be unique across the system.
        password (str): The password chosen by the user. Should follow security best practices in terms of complexity.
        username (str): The chosen username for the new user. This can be the same as the email or different.

    Returns:
        UserRegistrationResponse: A simple model to confirm successful registration or provide error messages. This model can be extended to include user ID or initial profile settings.
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        return UserRegistrationResponse(
            success=False, message="Email already registered."
        )
    hashed_password = bcrypt.hash(password)
    default_role = prisma.enums.RoleName.Individual
    try:
        user = await prisma.models.User.prisma().create(
            data={
                "email": email,
                "passwordHash": hashed_password,
                "roleName": default_role,
            }
        )
        return UserRegistrationResponse(
            success=True, message="User successfully registered.", user_id=user.id
        )
    except Exception as e:
        return UserRegistrationResponse(
            success=False, message=f"Failed to register user: {str(e)}"
        )
