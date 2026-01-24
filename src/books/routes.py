from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from src.books.schema import Book, BookCreateModel, BookUpdateModel
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session


book_router = APIRouter()
book_service = BookService()


@book_router.get("/", response_model=List[Book])
async def get_all_books(db_session: AsyncSession = Depends(get_session)) -> List[Book]:
    return await book_service.get_all_books(db_session)


@book_router.get("/{book_id}", response_model=Book)
async def view_book_detail(
    book_id: str, db_session: AsyncSession = Depends(get_session)
) -> dict:
    book = await book_service.get_a_book(book_id, db_session)
    if book is not None:
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found",
    )


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(
    payload: BookCreateModel, db_session: AsyncSession = Depends(get_session)
) -> dict:
    new_book = await book_service.create_book(payload, db_session)
    return new_book


@book_router.patch("/{book_id}", response_model=Book)
async def update_book(
    book_id: str,
    payload: BookUpdateModel,
    db_session: AsyncSession = Depends(get_session),
) -> dict:
    updated_book = await book_service.update_book(book_id, payload, db_session)
    if updated_book is not None:
        return updated_book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found",
    )


@book_router.delete(
    "/{book_id}", status_code=status.HTTP_204_NO_CONTENT, response_model={}
)
async def delete_book(
    book_id: str, db_session: AsyncSession = Depends(get_session)
) -> dict:
    deleted_book = await book_service.delete_book(book_id, db_session)
    if deleted_book is not None:
        return {}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found",
    )
