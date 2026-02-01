from datetime import datetime, timedelta
import random
from typing import Optional, List
from fastapi import HTTPException, status
from odmantic import ObjectId

from core.models.user_model import User, UserStatus, UserRole, UserAddress
from core.apis.schemas.requests.user_schema import UserCreate
from commons.auth import get_password_hash, verify_password, create_access_token
from core.database.database import get_engine
from commons.loggers import logger


logging = logger(__name__)


class UserController:
    @property
    def engine(self):
        return get_engine()

    async def register_user(self, user_data: UserCreate):
        """Register a new user"""
        # Check if user already exists
        existing_user = await self.engine.find_one(User, User.email == user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        # Hash password
        hashed_password = get_password_hash(user_data.password)

        # Map Address if provided
        user_address = None
        if user_data.address:
            user_address = UserAddress(
                street_address=user_data.address.street,
                city=user_data.address.city,
                state=user_data.address.state,
                postal_code=user_data.address.pincode,
                country=user_data.address.country or "India",
            )

        # Create user model
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            mobile_number=user_data.mobile_number,
            hashed_password=hashed_password,
            address=user_address,
            status=UserStatus.ACTIVE,
            role=UserRole.CUSTOMER,
        )

        # Save to database
        await self.engine.save(user)
        logging.info(f"User registered: {user.email}")

        # Convert to dict for proper serialization
        user_dict = user.model_dump()
        user_dict["id"] = str(user.id)
        return user_dict

    async def login_user(self, login_data: dict) -> dict:
        """Authenticate user and return token"""
        email = login_data.get("email")
        password = login_data.get("password")

        user = await self.engine.find_one(User, User.email == email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user.status == UserStatus.BLOCKED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Account is blocked"
            )

        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role}
        )

        # Convert user to dict for proper serialization
        user_dict = user.model_dump()
        user_dict["id"] = str(user.id)

        return {"access_token": access_token, "token_type": "bearer", "user": user_dict}

    async def get_user_profile(self, user_id: str):
        """Get user profile by ID"""
        try:
            user = await self.engine.find_one(User, User.id == ObjectId(user_id))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid User ID"
            )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Convert to dict for proper serialization
        user_dict = user.model_dump()
        user_dict["id"] = str(user.id)
        return user_dict

    async def update_user_profile(self, user_id: str, update_data: dict):
        """Update user profile - only allowed fields"""
        user = await self.get_user_profile(user_id)

        # Convert back to User model if it's a dict
        if isinstance(user, dict):
            user = await self.engine.find_one(User, User.id == ObjectId(user_id))

        # Sanitize white-list of fields that can be updated directly
        allowed_fields = ["first_name", "last_name", "mobile_number"]

        updated = False
        for field in allowed_fields:
            if field in update_data and update_data[field] is not None:
                setattr(user, field, update_data[field])
                updated = True

        if updated:
            user.updated_at = datetime.utcnow()
            await self.engine.save(user)

        # Convert to dict for proper serialization
        user_dict = user.model_dump()
        user_dict["id"] = str(user.id)
        return user_dict

    async def forgot_password(self, email: str) -> dict:
        """Initiate password reset with OTP"""
        user = await self.engine.find_one(User, User.email == email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)

        await self.engine.save(user)

        # In a real app, send OTP via email/SMS here
        logging.info(f"OTP for {email}: {otp}")

        return {"message": "OTP sent to your email"}

    async def reset_password(self, reset_data: dict) -> dict:
        """Reset password using OTP"""
        email = reset_data.get("email")
        otp = reset_data.get("otp")
        new_password = reset_data.get("new_password")

        user = await self.engine.find_one(User, User.email == email)
        if not user or user.otp != otp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP or email"
            )

        if user.otp_expiry < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired"
            )

        user.hashed_password = get_password_hash(new_password)
        user.otp = None
        user.otp_expiry = None
        user.updated_at = datetime.utcnow()
        await self.engine.save(user)

        return {"message": "Password reset successful"}

    async def delete_user(self, user_id: str) -> dict:
        """Delete user by ID"""
        # First verify user exists
        await self.get_user_profile(user_id)
        # Get actual User object for deletion
        user = await self.engine.find_one(User, User.id == ObjectId(user_id))
        await self.engine.delete(user)
        return {"message": "User deleted successfully"}

    async def get_all_users(self):
        """List all users (Admin)"""
        users = await self.engine.find(User)
        result = []
        for user in users:
            user_dict = user.model_dump()
            user_dict["id"] = str(user.id)
            result.append(user_dict)
        return result
