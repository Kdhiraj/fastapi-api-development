from sqlmodel import desc, select
from fastapi.exceptions import HTTPException
from fastapi import status
from src.reviews.schema import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Review
from typing import List
from src.auth.service import UserService
from src.books.service import BookService

user_service = UserService()
book_service = BookService()


class ReviewService:
    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ) -> Review:
        try:
            user = await user_service.get_user_by_email(user_email, session)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )

            book = await book_service.get_a_book(book_uid, session)
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
                )

            review_data_dict = review_data.model_dump()
            new_review = Review(
                **review_data_dict, user_uid=user.uid, book_uid=book_uid
            )

            new_review.user = user
            new_review.book = book
            session.add(new_review)
            await session.commit()
            await session.refresh(new_review)
            return new_review
        except Exception as e:
            await session.rollback()
            raise e

    async def get_books_reviews(
        self, book_uid: str, session: AsyncSession
    ) -> List[Review]:
        statement = (
            select(Review)
            .where(Review.book_uid == book_uid)
            .order_by(desc(Review.created_at))
        )
        result = await session.execute(statement)
        return result.scalars().all()
