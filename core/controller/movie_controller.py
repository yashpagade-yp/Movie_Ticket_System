from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from odmantic import ObjectId

from core.models.movie_model import Movie, MovieStatus
from core.apis.schemas.requests.movie_schema import MovieCreate, MovieUpdate
from core.database.database import get_engine
from commons.loggers import logger

logging = logger(__name__)


class MovieController:
    @property
    def engine(self):
        return get_engine()

    async def create_movie(self, movie_data: MovieCreate) -> Movie:
        """Create a new movie"""
        movie = Movie(**movie_data.model_dump())
        await self.engine.save(movie)
        logging.info(f"Movie created: {movie.title}")
        return movie

    async def get_movie(self, movie_id: str) -> Movie:
        """Get movie by ID"""
        try:
            movie = await self.engine.find_one(Movie, Movie.id == ObjectId(movie_id))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Movie ID"
            )

        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
            )
        return movie

    async def get_all_movies(
        self, status_filter: Optional[MovieStatus] = None
    ) -> List[Movie]:
        """List all movies with optional status filter"""
        if status_filter:
            return await self.engine.find(Movie, Movie.status == status_filter)
        return await self.engine.find(Movie)

    async def update_movie(self, movie_id: str, update_data: MovieUpdate) -> Movie:
        """Update movie details"""
        movie = await self.get_movie(movie_id)

        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(movie, field, value)

        movie.updated_at = datetime.utcnow()
        await self.engine.save(movie)
        logging.info(f"Movie updated: {movie.title}")
        return movie

    async def delete_movie(self, movie_id: str) -> dict:
        """Delete movie by ID"""
        movie = await self.get_movie(movie_id)
        await self.engine.delete(movie)
        logging.info(f"Movie deleted: {movie.title}")
        return {"message": "Movie deleted successfully"}
