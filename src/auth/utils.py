from fastapi import logger
from pwdlib import PasswordHash
from datetime import timedelta, datetime
import jwt
import uuid
from src.config import Config


passwd_context = PasswordHash.recommended()

ACCESS_TOKEN_EXPIRY_MINUTES = 3600


def hash_password(password: str) -> str:
    return passwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return passwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
) -> str:
    """Create a JWT access token."""
    payload = {}
    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry else timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM,
    )
    return token


def decode_access_token(token: str) -> dict:
    """Decode a JWT access token."""
    try:
        payload = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM],
        )
        return payload
    except jwt.PyJWTError as e:
        logger.error(f"JWT Error: {e}")
        return None
