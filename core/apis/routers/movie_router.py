from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional

from core.models.movie_model import MovieStatus
from core.apis.schemas.requests.movie_schema import MovieCreate, MovieUpdate
from core.apis.schemas.responses.user_responses import MovieResponse
from core.controller.movie_controller import MovieController
from commons.auth import get_current_user, require_admin

movie_router = APIRouter()
movie_controller = MovieController()


@movie_router.post(
    "/", response_model=MovieResponse, status_code=status.HTTP_201_CREATED
)
async def create_movie(movie_data: MovieCreate, admin: dict = Depends(require_admin)):
    """Admin only: Create a new movie"""
    return await movie_controller.create_movie(movie_data)


@movie_router.get("/", response_model=List[MovieResponse])
async def get_movies(status: Optional[MovieStatus] = Query(None)):
    """Public: Get all movies with optional status filter"""
    return await movie_controller.get_all_movies(status)


@movie_router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: str):
    """Public: Get a specific movie by ID"""
    return await movie_controller.get_movie(movie_id)


@movie_router.put("/{movie_id}", response_model=MovieResponse)
async def update_movie(
    movie_id: str, update_data: MovieUpdate, admin: dict = Depends(require_admin)
):
    """Admin only: Update movie details"""
    return await movie_controller.update_movie(movie_id, update_data)


@movie_router.delete("/{movie_id}")
async def delete_movie(movie_id: str, admin: dict = Depends(require_admin)):
    """Admin only: Delete a movie"""
    return await movie_controller.delete_movie(movie_id)
