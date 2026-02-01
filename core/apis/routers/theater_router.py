from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional

from core.apis.schemas.requests.theater_schema import (
    TheaterCreate,
    TheaterUpdate,
    ScreenCreate,
)
from core.apis.schemas.responses.user_responses import TheaterResponse
from core.controller.theater_controller import TheaterController
from commons.auth import get_current_user, require_admin

theater_router = APIRouter()
theater_controller = TheaterController()


@theater_router.post(
    "/", response_model=TheaterResponse, status_code=status.HTTP_201_CREATED
)
async def create_theater(
    theater_data: TheaterCreate, current_user: dict = Depends(get_current_user)
):
    """Authenticated users (Owners): Create a new theater"""
    # In a real app, we'd check if the user has the THEATER_OWNER role
    owner_id = current_user.get("sub")
    return await theater_controller.create_theater(theater_data, owner_id)


@theater_router.get("/", response_model=List[TheaterResponse])
async def get_theaters(location: Optional[str] = Query(None)):
    """Public: Get all theaters with optional location filter"""
    return await theater_controller.get_all_theaters(location)


@theater_router.get("/{theater_id}", response_model=TheaterResponse)
async def get_theater(theater_id: str):
    """Public: Get a specific theater by ID"""
    return await theater_controller.get_theater(theater_id)


@theater_router.put("/{theater_id}", response_model=TheaterResponse)
async def update_theater(
    theater_id: str,
    update_data: TheaterUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Authenticated users: Update theater details"""
    # Real app would check if current_user is the owner
    return await theater_controller.update_theater(theater_id, update_data)


@theater_router.delete("/{theater_id}")
async def delete_theater(
    theater_id: str, current_user: dict = Depends(get_current_user)
):
    """Authenticated users: Delete a theater"""
    return await theater_controller.delete_theater(theater_id)


# --- Screen Endpoints ---


@theater_router.post("/{theater_id}/screens", status_code=status.HTTP_201_CREATED)
async def add_screen(
    theater_id: str,
    screen_data: ScreenCreate,
    current_user: dict = Depends(get_current_user),
):
    """Authenticated users: Add a screen to their theater"""
    return await theater_controller.add_screen(theater_id, screen_data)


@theater_router.get("/{theater_id}/screens")
async def get_screens(theater_id: str):
    """Public: Get all screens for a theater"""
    return await theater_controller.get_theater_screens(theater_id)


@theater_router.delete("/screens/{screen_id}")
async def delete_screen(screen_id: str, current_user: dict = Depends(get_current_user)):
    """Authenticated users: Delete a screen"""
    return await theater_controller.delete_screen(screen_id)
