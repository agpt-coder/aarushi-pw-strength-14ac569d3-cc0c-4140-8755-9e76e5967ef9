from datetime import datetime, timedelta

import prisma
import prisma.models
from pydantic import BaseModel


class RateLimitConfigurationResponse(BaseModel):
    """
    Response model that confirms the new rate limiting configuration.
    """

    status: str
    applied_endpoint: str
    applied_limit: int
    applied_window: int


async def manage_rate_limiting(
    endpoint: str, limit: int, window: int
) -> RateLimitConfigurationResponse:
    """
    Endpoint to configure rate limiting parameters.

    Args:
        endpoint (str): The specific API endpoint pattern to apply rate limiting to. Use '*' for global configuration.
        limit (int): The maximum number of requests allowed within the specified time window.
        window (int): The time window in seconds over which the rate limit applies.

    Returns:
        RateLimitConfigurationResponse: Response model that confirms the new rate limiting configuration.
    """
    period_end = datetime.now() + timedelta(seconds=window)
    existing_rate_limit = await prisma.models.RateLimit.prisma().find_first(
        where={"endpoint": endpoint}
    )
    if existing_rate_limit:
        await prisma.models.RateLimit.prisma().update(
            where={"id": existing_rate_limit.id},
            data={"limit": limit, "period": period_end},
        )
        status = "updated"
    else:
        await prisma.models.RateLimit.prisma().create(
            data={
                "endpoint": endpoint,
                "limit": limit,
                "period": period_end,
                "createdAt": datetime.now(),
                "updatedAt": datetime.now(),
            }
        )
        status = "created"
    return RateLimitConfigurationResponse(
        status=status,
        applied_endpoint=endpoint,
        applied_limit=limit,
        applied_window=window,
    )
