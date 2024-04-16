import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.analyze_password_service
import project.generate_api_key_service
import project.manage_rate_limiting_service
import project.password_reset_service
import project.register_user_service
import project.update_profile_service
import project.user_login_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="aarushi-pw-strength-1",
    lifespan=lifespan,
    description="To address the task, the system should implement an endpoint capable of accepting a password string and analyzing its strength. This analysis would involve evaluating the password based on several factors including its length, complexity (use of uppercase and lowercase letters, numbers, and special symbols), and its adherence to or deviation from common patterns which attackers might easily guess (e.g., '123456', 'password', 'qwerty'). The endpoint should then assign a score indicating the password's strength, with categories such as weak, medium, strong, or very strong. The scoring algorithm should be designed to encourage users towards creating passwords that are hard to guess or brute-force by attackers, incorporating findings from previous searches and user inputs. Based on the evaluation, the service should also offer actionable suggestions for improving password security, such as increasing length, diversifying characters, and avoiding common patterns or personal information. Best practices include not only these technical measures but also encouraging behavior like regular password updates, the use of different passwords for different sites, and the activation of multi-factor authentication where possible. For implementation, using Python and the FastAPI framework can facilitate rapid development, with PostgreSQL for database needs and Prisma as the ORM to interact with the database efficiently. This solution aims not just to evaluate passwords but also to educate users about creating stronger, more secure passwords, thus enhancing overall security.",
)


@app.post("/user/login", response_model=project.user_login_service.UserLoginResponse)
async def api_post_user_login(
    email: str, password: str
) -> project.user_login_service.UserLoginResponse | Response:
    """
    Endpoint for user login and authentication.
    """
    try:
        res = await project.user_login_service.user_login(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user/password/reset",
    response_model=project.password_reset_service.PasswordResetResponse,
)
async def api_post_password_reset(
    email: str,
) -> project.password_reset_service.PasswordResetResponse | Response:
    """
    Endpoint for users to reset their password.
    """
    try:
        res = await project.password_reset_service.password_reset(email)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/generateKey",
    response_model=project.generate_api_key_service.GenerateApiKeyResponse,
)
async def api_post_generate_api_key(
    user_id: str, description: Optional[str]
) -> project.generate_api_key_service.GenerateApiKeyResponse | Response:
    """
    Endpoint for generating a new API key for external developers.
    """
    try:
        res = await project.generate_api_key_service.generate_api_key(
            user_id, description
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/profile/update",
    response_model=project.update_profile_service.UpdateUserProfileResponse,
)
async def api_put_update_profile(
    email: str, name: str, profile_picture: Optional[str]
) -> project.update_profile_service.UpdateUserProfileResponse | Response:
    """
    Allows users to update their profile information.
    """
    try:
        res = await project.update_profile_service.update_profile(
            email, name, profile_picture
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/api/rateLimit/configure",
    response_model=project.manage_rate_limiting_service.RateLimitConfigurationResponse,
)
async def api_put_manage_rate_limiting(
    endpoint: str, limit: int, window: int
) -> project.manage_rate_limiting_service.RateLimitConfigurationResponse | Response:
    """
    Endpoint to configure rate limiting parameters.
    """
    try:
        res = await project.manage_rate_limiting_service.manage_rate_limiting(
            endpoint, limit, window
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/password/analyze",
    response_model=project.analyze_password_service.PasswordAnalysisResponse,
)
async def api_post_analyze_password(
    password: str,
) -> project.analyze_password_service.PasswordAnalysisResponse | Response:
    """
    Endpoint for evaluating the strength of a submitted password.
    """
    try:
        res = project.analyze_password_service.analyze_password(password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user/register",
    response_model=project.register_user_service.UserRegistrationResponse,
)
async def api_post_register_user(
    email: str, password: str, username: str
) -> project.register_user_service.UserRegistrationResponse | Response:
    """
    Endpoint to register a new user.
    """
    try:
        res = await project.register_user_service.register_user(
            email, password, username
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
