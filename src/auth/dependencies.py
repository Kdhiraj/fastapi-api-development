from typing import List
from fastapi import Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .utils import decode_access_token
from src.db.redis import is_token_in_blocklist
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from .service import UserService
from src.errors import (
    InvalidToken,
    RefreshTokenRequired,
    AccessTokenRequired,
    InsufficientPermission,
    UserNotFound,
)

user_service = UserService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_access_token(token)

        if not token or not self.token_valid(token):
            raise InvalidToken()

        if await is_token_in_blocklist(token_data["jti"]):
            raise InvalidToken()

        self.verify_token_data(token_data)
        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_access_token(token)
        return token_data is not None

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("Subclasses must implement this method")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise RefreshTokenRequired()


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
) -> dict:
    user_email = token_details["user"]["email"]
    user = await user_service.get_user_by_email(user_email, session)
    if not user:
        raise UserNotFound()
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: dict = Depends(get_current_user)) -> bool:
        if current_user.role in self.allowed_roles:
            return True
        raise InsufficientPermission()
