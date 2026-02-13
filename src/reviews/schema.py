from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, Field


class ReviewModel(BaseModel):
    uid: uuid.UUID
    book_uid: uuid.UUID
    user_uid: Optional[uuid.UUID] = None
    rating: float = Field(lt=5)
    review_txt: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ReviewCreateModel(BaseModel):
    rating: float = Field(lt=5)
    review_txt: Optional[str] = None
