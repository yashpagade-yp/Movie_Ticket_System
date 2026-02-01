from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from core.models.user_model import UserRole, UserStatus


class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    mobile_number: str
    role: UserRole
    status: UserStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class MovieResponse(BaseModel):
    id: str
    title: str
    description: str
    language: str
    genres: List[str]
    duration_minutes: int
    release_date: datetime
    poster_url: Optional[str]
    trailer_url: Optional[str]
    status: str

    class Config:
        populate_by_name = True
        from_attributes = True


class TheaterResponse(BaseModel):
    id: str
    name: str
    location: str
    address: str
    contact_number: Optional[str]
    is_active: bool

    class Config:
        populate_by_name = True
        from_attributes = True


class ShowtimeResponse(BaseModel):
    id: str
    movie_id: str
    theater_id: str
    screen_id: str
    start_time: datetime
    end_time: datetime
    base_price: float
    is_active: bool

    class Config:
        populate_by_name = True
        from_attributes = True


class BookingResponse(BaseModel):
    id: str
    user_id: str
    showtime_id: str
    seats: List[str]
    total_amount: float
    status: str
    booking_time: datetime

    class Config:
        populate_by_name = True
        from_attributes = True


class TransactionResponse(BaseModel):
    id: str
    booking_id: str
    user_id: str
    amount: float
    currency: str
    payment_method: Optional[str]
    status: str
    gateway_transaction_id: Optional[str]
    created_at: datetime

    class Config:
        populate_by_name = True
        from_attributes = True
