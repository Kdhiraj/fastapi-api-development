from sqlmodel.ext.asyncio.session import AsyncSession
from .models import User
from .schemas import UserCreateModel
from sqlmodel import select
from src.auth.utils import hash_password


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        """Retrieve a user by email."""
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        result = result.scalars().first()
        return result

    async def user_exist(self, email: str, session: AsyncSession):
        """Check if a user exists by email."""
        user = await self.get_user_by_email(email, session)
        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        """Create a new user in the database."""
        user_data_dict = user_data.model_dump()

        new_user = User(
            **user_data_dict,
        )
        new_user.password_hash = hash_password(user_data_dict["password"])
        new_user.role = "user"
        session.add(new_user)
        await session.commit()
        return new_user
