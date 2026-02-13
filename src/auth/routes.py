from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    RoleChecker,
    get_current_user,
)
from src.db.main import get_session
from .schemas import UserBooksModel, UserCreateModel, UserLoginModel, UserModel
from .service import UserService
from .utils import verify_password, create_access_token
from datetime import datetime, timedelta
from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service = UserService()
REFRESH_TOKEN_EXPIRY_IN_DAYS = 2
role_checker = RoleChecker(allowed_roles=["admin", "user"])


@auth_router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=UserModel
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    is_user_exist = await user_service.user_exist(email, session)

    if is_user_exist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )

    new_user = await user_service.create_user(user_data, session)
    return new_user


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            user_data = {
                "email": user.email,
                "user_uid": str(user.uid),
                "role": user.role,
            }
            access_token = create_access_token(user_data=user_data)

            refresh_token = create_access_token(
                user_data=user_data,
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY_IN_DAYS),
            )

            return JSONResponse(
                content={
                    "success": True,
                    "message": "Login successful",
                    "user": user_data,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
    )


@auth_router.get("/refresh_token", status_code=status.HTTP_200_OK)
async def get_new_access_token(
    token_data: dict = Depends(RefreshTokenBearer()),
):
    expiry_date = token_data.get("exp")
    if datetime.fromtimestamp(expiry_date) < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired, please login again",
        )
    user_data = token_data.get("user")
    new_access_token = create_access_token(user_data=user_data)
    return JSONResponse(
        content={
            "access_token": new_access_token,
        }
    )


@auth_router.post("/logout")
async def logout(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details.get("jti")
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={
            "message": "Successfully logged out",
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(
    current_user: dict = Depends(get_current_user), _: bool = Depends(role_checker)
):
    return current_user


@auth_router.post("/reset-password")
async def reset_password():
    return {"message": "Reset Password endpoint"}


@auth_router.post("/verify-email")
async def verify_email():
    return {"message": "Verify Email endpoint"}


@auth_router.post("/change-password")
async def change_password():
    return {"message": "Change Password endpoint"}
