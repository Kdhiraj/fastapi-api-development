import uuid
from sqlmodel import Column, SQLModel, Field
from datetime import datetime, timezone
import sqlalchemy.dialects.postgresql as pg


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            index=True,
            default=uuid.uuid4,
        )
    )
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    is_verified: bool = Field(default=False)

    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=lambda: datetime.now(datetime.timezone.utc),
        )
    )

    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
        )
    )

    def __repr__(self):
        return f"<User {self.username}>"
