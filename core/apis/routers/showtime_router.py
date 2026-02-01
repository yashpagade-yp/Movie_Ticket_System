from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional

from core.apis.schemas.requests.showtime_schema import ShowtimeCreate, ShowtimeUpdate
from core.apis.schemas.responses.user_responses import ShowtimeResponse
from core.controller.showtime_controller import ShowtimeController
from commons.auth import get_current_user, require_admin

showtime_router = APIRouter()
showtime_controller = ShowtimeController()


@showtime_router.post(
    "/", response_model=ShowtimeResponse, status_code=status.HTTP_201_CREATED
)
async def create_showtime(
    showtime_data: ShowtimeCreate, admin: dict = Depends(require_admin)
):
    """Admin only: Create a new showtime"""
    return await showtime_controller.create_showtime(showtime_data)


@showtime_router.get("/", response_model=List[ShowtimeResponse])
async def get_all_showtimes(
    movie_id: Optional[str] = Query(None), theater_id: Optional[str] = Query(None)
):
    """Public: Get showtimes with optional movie or theater filters"""
    if movie_id:
        return await showtime_controller.get_movie_showtimes(movie_id)
    if theater_id:
        return await showtime_controller.get_theater_showtimes(theater_id)
    # Could add general find all if needed
    return []


@showtime_router.get("/{showtime_id}", response_model=ShowtimeResponse)
async def get_showtime(showtime_id: str):
    """Public: Get a specific showtime by ID"""
    return await showtime_controller.get_showtime(showtime_id)


@showtime_router.put("/{showtime_id}", response_model=ShowtimeResponse)
async def update_showtime(
    showtime_id: str, update_data: ShowtimeUpdate, admin: dict = Depends(require_admin)
):
    """Admin only: Update showtime details"""
    return await showtime_controller.update_showtime(showtime_id, update_data)


@showtime_router.delete("/{showtime_id}")
async def delete_showtime(showtime_id: str, admin: dict = Depends(require_admin)):
    """Admin only: Delete a showtime"""
    return await showtime_controller.delete_showtime(showtime_id)
