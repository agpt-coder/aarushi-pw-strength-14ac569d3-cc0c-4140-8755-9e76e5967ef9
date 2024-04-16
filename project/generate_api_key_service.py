import secrets
from datetime import datetime, timedelta
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class GenerateApiKeyResponse(BaseModel):
    """
    Response model containing the generated API key details.
    """

    api_key: str
    issued_at: datetime
    expires_at: Optional[datetime] = None


async def generate_api_key(
    user_id: str, description: Optional[str]
) -> GenerateApiKeyResponse:
    """
    Endpoint for generating a new API key for external developers.

    Args:
    user_id (str): Identifier of the user requesting the API key. This could be extracted from the authentication token rather than being directly provided.
    description (Optional[str]): A brief description or metadata about how the API key will be used, provided by the user.

    Returns:
    GenerateApiKeyResponse: Response model containing the generated API key details.
    """
    new_api_key = secrets.token_urlsafe(32)
    expiry_date = datetime.now() + timedelta(days=30)
    saved_api_key = await prisma.models.APIKey.prisma().create(
        data={
            "key": new_api_key,
            "userId": user_id,
            "issuedAt": datetime.now(),
            "expiresAt": expiry_date,
        }
    )
    response = GenerateApiKeyResponse(
        api_key=new_api_key,
        issued_at=saved_api_key.issuedAt,
        expires_at=saved_api_key.expiresAt,
    )
    return response
