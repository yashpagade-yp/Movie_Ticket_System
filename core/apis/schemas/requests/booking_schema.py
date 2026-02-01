from pydantic import BaseModel, Field
from typing import List, Optional
from core.models.booking_model import BookingStatus


class BookingCreate(BaseModel):
    showtime_id: str = Field(..., description="Showtime ID (hex string)")
    seats: List[str] = Field(..., min_items=1, description="List of seat labels")


class BookingUpdate(BaseModel):
    status: BookingStatus
