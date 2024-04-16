from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    Confirms whether the profile update was successful and reflects the updated profile information.
    """

    success: bool
    message: str


async def update_profile(
    email: str, name: str, profile_picture: Optional[str]
) -> UpdateUserProfileResponse:
    """
    Allows users to update their profile information.

    Args:
        email (str): New email address for the user. Must be valid and unique across the system.
        name (str): New name for the user. This is not strictly required to be unique.
        profile_picture (Optional[str]): URL to the new profile picture. Must be a valid URL format.

    Returns:
        UpdateUserProfileResponse: Confirms whether the profile update was successful and reflects the updated profile information.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user:
        return UpdateUserProfileResponse(success=False, message="User not found.")
    try:
        await prisma.models.User.prisma().update(
            where={"email": email},
            data={"name": name, "profilePicture": profile_picture},
        )
        return UpdateUserProfileResponse(
            success=True, message="Profile updated successfully."
        )
    except Exception as e:
        return UpdateUserProfileResponse(
            success=False, message=f"Failed to update profile. Error: {e}"
        )
