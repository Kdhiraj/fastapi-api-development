from fastapi import APIRouter, Depends, status
from src.db.models import User
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer, RoleChecker, get_current_user
from src.reviews.schema import ReviewCreateModel, ReviewModel
from src.reviews.service import ReviewService
from typing import List

review_router = APIRouter()
access_token_bearer = AccessTokenBearer()
review_service = ReviewService()
role_checker = Depends(RoleChecker(allowed_roles=["admin", "user"]))


@review_router.get(
    "/{book_uid}", response_model=List[ReviewModel], dependencies=[role_checker]
)
async def get_book_reviews(
    book_uid: str,
    db_session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
) -> dict:
    reviews = await review_service.get_books_reviews(book_uid, db_session)
    return reviews


@review_router.post(
    "/books/{book_uid}",
    status_code=status.HTTP_201_CREATED,
    response_model=ReviewModel,
    dependencies=[role_checker],
)
async def create_review(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session),
) -> dict:
    new_review = await review_service.add_review_to_book(
        user_email=current_user.email,
        book_uid=book_uid,
        review_data=review_data,
        session=db_session,
    )
    return new_review
