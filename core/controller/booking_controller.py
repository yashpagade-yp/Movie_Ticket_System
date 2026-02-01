from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import HTTPException, status
from odmantic import ObjectId

from core.models.booking_model import Booking, BookingStatus
from core.models.showtime_model import Showtime
from core.apis.schemas.requests.booking_schema import BookingCreate, BookingUpdate
from core.database.database import get_engine
from commons.loggers import logger

logging = logger(__name__)


class BookingController:
    @property
    def engine(self):
        return get_engine()

    async def create_booking(
        self, booking_data: BookingCreate, user_id: str
    ) -> Booking:
        """Create a new ticket booking"""
        # Validate showtime
        showtime = await self.engine.find_one(
            Showtime, Showtime.id == ObjectId(booking_data.showtime_id)
        )
        if not showtime:
            raise HTTPException(status_code=404, detail="Showtime not found")

        if not showtime.is_active:
            raise HTTPException(status_code=400, detail="Showtime is no longer active")

        # Check for seat availability (Simplified logic)
        # In a real app, we would check existing confirmed/pending bookings for this showtime
        # to ensure the same seats aren't double-booked.

        # Calculate total amount
        total_amount = showtime.base_price * len(booking_data.seats)

        booking = Booking(
            user_id=ObjectId(user_id),
            showtime_id=ObjectId(booking_data.showtime_id),
            seats=booking_data.seats,
            total_amount=total_amount,
            status=BookingStatus.PENDING,
            expires_at=datetime.utcnow()
            + timedelta(minutes=15),  # Expire if not paid in 15 mins
        )

        await self.engine.save(booking)
        logging.info(
            f"Booking created for user {user_id} - Seats: {booking_data.seats}"
        )
        return booking

    async def get_booking(self, booking_id: str) -> Booking:
        """Get booking by ID"""
        try:
            booking = await self.engine.find_one(
                Booking, Booking.id == ObjectId(booking_id)
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Booking ID"
            )

        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found"
            )
        return booking

    async def get_user_bookings(self, user_id: str) -> List[Booking]:
        """List all bookings for a specific user"""
        return await self.engine.find(Booking, Booking.user_id == ObjectId(user_id))

    async def update_booking_status(
        self, booking_id: str, update_data: BookingUpdate
    ) -> Booking:
        """Update booking status (Confirmed/Cancelled)"""
        booking = await self.get_booking(booking_id)

        booking.status = update_data.status
        await self.engine.save(booking)
        logging.info(
            f"Booking status updated to {update_data.status} for booking {booking_id}"
        )
        return booking

    async def cancel_booking(self, booking_id: str, user_id: str) -> dict:
        """Cancel a booking if allowed"""
        booking = await self.get_booking(booking_id)

        if str(booking.user_id) != user_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to cancel this booking"
            )

        if booking.status == BookingStatus.CANCELLED:
            return {"message": "Booking is already cancelled"}

        booking.status = BookingStatus.CANCELLED
        await self.engine.save(booking)
        logging.info(f"Booking {booking_id} cancelled by user")
        return {"message": "Booking cancelled successfully"}
