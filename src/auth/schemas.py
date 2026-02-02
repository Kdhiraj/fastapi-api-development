from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
import uuid


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password_hash: str = Field(exclude=True)
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserCreateModel(BaseModel):
    username: str = Field(..., min_length=3, max_length=15)
    first_name: str = Field(..., min_length=1, max_length=15)
    last_name: str = Field(..., min_length=1, max_length=15)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str
