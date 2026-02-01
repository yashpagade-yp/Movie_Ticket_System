from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional

from core.apis.schemas.requests.booking_schema import BookingCreate, BookingUpdate
from core.apis.schemas.responses.user_responses import BookingResponse
from core.controller.booking_controller import BookingController
from commons.auth import get_current_user, require_admin

booking_router = APIRouter()
booking_controller = BookingController()


@booking_router.post(
    "/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED
)
async def create_booking(
    booking_data: BookingCreate, current_user: dict = Depends(get_current_user)
):
    """Authenticated Users: Book tickets"""
    user_id = current_user.get("sub")
    return await booking_controller.create_booking(booking_data, user_id)


@booking_router.get("/my-bookings", response_model=List[BookingResponse])
async def get_my_bookings(current_user: dict = Depends(get_current_user)):
    """Authenticated Users: See their own bookings"""
    user_id = current_user.get("sub")
    return await booking_controller.get_user_bookings(user_id)


@booking_router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: str, current_user: dict = Depends(get_current_user)):
    """Authenticated Users: Get specific booking details"""
    # Real app would check if user owns the booking
    return await booking_controller.get_booking(booking_id)


@booking_router.patch("/{booking_id}/cancel")
async def cancel_booking(
    booking_id: str, current_user: dict = Depends(get_current_user)
):
    """Authenticated Users: Cancel their booking"""
    user_id = current_user.get("sub")
    return await booking_controller.cancel_booking(booking_id, user_id)


@booking_router.put("/{booking_id}/status", response_model=BookingResponse)
async def update_status(
    booking_id: str, update_data: BookingUpdate, admin: dict = Depends(require_admin)
):
    """Admin Only: Update booking status manually"""
    return await booking_controller.update_booking_status(booking_id, update_data)
