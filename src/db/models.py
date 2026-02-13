import uuid
from typing import List, Optional
from sqlmodel import Column, Relationship, SQLModel, Field
from datetime import datetime, timezone, date
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
    password_hash: str
    is_verified: bool = Field(default=False)
    role: str = Field(
        sa_column=Column(pg.VARCHAR(length=50), nullable=False, server_default="user")
    )

    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=lambda: datetime.now(timezone.utc),
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
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            index=True,
            default=uuid.uuid4,
        )
    )

    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="users.uid",
    )

    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=lambda: datetime.now(timezone.utc),
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
    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<Book(title={self.title}, author={self.author})>"


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            index=True,
            default=uuid.uuid4,
        )
    )
    review_txt: str
    rating: float = Field(lt=5.0)
    user_uid: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="users.uid",
    )
    book_uid: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="books.uid",
    )
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=lambda: datetime.now(timezone.utc),
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
    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review(review_txt={self.review_txt}, rating={self.rating} by user {self.user_uid} for book {self.book_uid})>"
