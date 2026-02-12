from redis.asyncio import Redis
from src.config import Config

token_blocklist = Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,
)
JTI_EXPIRATION_SECONDS = 3600  # 1 hour


async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="true", ex=JTI_EXPIRATION_SECONDS)


async def is_token_in_blocklist(jti: str) -> bool:
    jti = await token_blocklist.get(jti)
    return jti is not None
