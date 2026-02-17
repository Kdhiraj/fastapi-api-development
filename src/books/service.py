from datetime import datetime
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from .schemas import BookCreateModel, BookUpdateModel


class BookService:
    async def get_all_books(self, db_session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await db_session.execute(statement)
        return result.scalars().all()

    async def get_user_books(self, user_uid: str, db_session: AsyncSession):
        statement = (
            select(Book)
            .where(Book.user_uid == user_uid)
            .order_by(desc(Book.created_at))
        )
        result = await db_session.execute(statement)
        return result.scalars().all()

    async def get_book(self, book_id: str, db_session: AsyncSession):
        statement = select(Book).where(Book.uid == book_id)
        result = await db_session.execute(statement)
        result = result.scalars().first()
        return result

    async def create_book(
        self, book: BookCreateModel, user_uid: str, db_session: AsyncSession
    ):
        book_data_dict = book.model_dump()
        new_book = Book(**book_data_dict)
        new_book.published_date = datetime.strptime(
            book_data_dict["published_date"], "%Y-%m-%d"
        )
        new_book.user_uid = user_uid
        db_session.add(new_book)
        await db_session.commit()
        await db_session.refresh(new_book)
        return new_book

    async def update_book(
        self, book_id: str, book: BookUpdateModel, db_session: AsyncSession
    ):
        existing_book = await self.get_a_book(book_id, db_session)
        update_data_dict = book.model_dump()
        if existing_book is not None:
            for k, v in update_data_dict.items():
                setattr(existing_book, k, v)
            await db_session.commit()
            await db_session.refresh(existing_book)
            return existing_book
        else:
            return None

    async def delete_book(self, book_id: str, db_session: AsyncSession):
        existing_book = await self.get_a_book(book_id, db_session)
        if existing_book is not None:
            await db_session.delete(existing_book)
            await db_session.commit()
            return existing_book
        else:
            return None
