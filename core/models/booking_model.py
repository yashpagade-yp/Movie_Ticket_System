from datetime import datetime
from enum import Enum
from typing import List, Optional
from odmantic import Field, Model, ObjectId


class BookingStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class Booking(Model):
    """
    Model representing a ticket booking.
    """

    user_id: ObjectId = Field(..., description="User who made the booking")
    showtime_id: ObjectId = Field(..., description="The specific showtime")

    # List of seat identifiers booked e.g. ["A1", "A2"]
    seats: List[str] = Field(..., min_items=1, description="List of booked seat labels")

    total_amount: float = Field(..., description="Total price for the booking")
    status: BookingStatus = Field(default=BookingStatus.PENDING)

    booking_time: datetime = Field(default_factory=datetime.utcnow)

    # Optional: Track expiry for pending bookings (e.g. if payment not done in 10 mins)
    expires_at: Optional[datetime] = Field(default=None)

    model_config = {"collection": "bookings"}
