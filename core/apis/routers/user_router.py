from fastapi import APIRouter, Depends, status
from typing import List

from core.apis.schemas.requests.user_schema import (
    UserCreate,
    UserLogin,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    UserUpdate,
)

from core.apis.schemas.responses.user_responses import UserResponse, LoginResponse
from core.controller.user_controller import UserController
from commons.auth import get_current_user, require_admin


user_router = APIRouter()
user_controller = UserController()


@user_router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserCreate):
    """Endpoint to register a new user"""
    return await user_controller.register_user(user_data)


@user_router.post("/login", response_model=LoginResponse)
async def login(login_data: UserLogin):
    """Endpoint to authenticate user and receive JWT token"""
    return await user_controller.login_user(login_data.model_dump())


@user_router.get("/me", response_model=UserResponse)
async def get_me(current_user_token: dict = Depends(get_current_user)):
    """Endpoint to get current logged-in user's profile"""
    user_id = current_user_token.get("sub")
    return await user_controller.get_user_profile(user_id)


@user_router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    """Endpoint to initiate password reset"""
    return await user_controller.forgot_password(request.email)


@user_router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    """Endpoint to reset password using OTP"""
    return await user_controller.reset_password(request.model_dump())


@user_router.put("/me", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate, current_user_token: dict = Depends(get_current_user)
):
    """Endpoint to update current logged-in user's profile"""
    user_id = current_user_token.get("sub")
    return await user_controller.update_user_profile(user_id, update_data.model_dump())


@user_router.delete("/me")
async def delete_me(current_user_token: dict = Depends(get_current_user)):
    """Endpoint to delete current logged-in user's account"""
    user_id = current_user_token.get("sub")
    return await user_controller.delete_user(user_id)


@user_router.get("/all", response_model=List[UserResponse])
async def get_all_users(admin: dict = Depends(require_admin)):
    """Endpoint for Admin to list all users"""
    return await user_controller.get_all_users()
