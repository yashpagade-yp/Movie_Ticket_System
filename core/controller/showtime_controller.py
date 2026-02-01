from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from odmantic import ObjectId

from core.models.showtime_model import Showtime
from core.models.movie_model import Movie
from core.models.theater_model import Theater, Screen
from core.apis.schemas.requests.showtime_schema import ShowtimeCreate, ShowtimeUpdate
from core.database.database import get_engine
from commons.loggers import logger

logging = logger(__name__)


class ShowtimeController:
    @property
    def engine(self):
        return get_engine()

    async def create_showtime(self, showtime_data: ShowtimeCreate) -> Showtime:
        """Create a new showtime"""
        # Validate existance of Movie, Theater, and Screen
        movie = await self.engine.find_one(
            Movie, Movie.id == ObjectId(showtime_data.movie_id)
        )
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        theater = await self.engine.find_one(
            Theater, Theater.id == ObjectId(showtime_data.theater_id)
        )
        if not theater:
            raise HTTPException(status_code=404, detail="Theater not found")

        screen = await self.engine.find_one(
            Screen, Screen.id == ObjectId(showtime_data.screen_id)
        )
        if not screen:
            raise HTTPException(status_code=404, detail="Screen not found")

        showtime = Showtime(
            movie_id=ObjectId(showtime_data.movie_id),
            theater_id=ObjectId(showtime_data.theater_id),
            screen_id=ObjectId(showtime_data.screen_id),
            start_time=showtime_data.start_time,
            end_time=showtime_data.end_time,
            base_price=showtime_data.base_price,
        )
        await self.engine.save(showtime)
        logging.info(
            f"Showtime created for movie {movie.title} at theater {theater.name}"
        )
        return showtime

    async def get_showtime(self, showtime_id: str) -> Showtime:
        """Get showtime by ID"""
        try:
            showtime = await self.engine.find_one(
                Showtime, Showtime.id == ObjectId(showtime_id)
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Showtime ID"
            )

        if not showtime:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found"
            )
        return showtime

    async def get_theater_showtimes(self, theater_id: str) -> List[Showtime]:
        """List all showtimes for a specific theater"""
        return await self.engine.find(
            Showtime, Showtime.theater_id == ObjectId(theater_id)
        )

    async def get_movie_showtimes(self, movie_id: str) -> List[Showtime]:
        """List all showtimes for a specific movie"""
        return await self.engine.find(Showtime, Showtime.movie_id == ObjectId(movie_id))

    async def update_showtime(
        self, showtime_id: str, update_data: ShowtimeUpdate
    ) -> Showtime:
        """Update showtime details"""
        showtime = await self.get_showtime(showtime_id)

        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(showtime, field, value)

        showtime.updated_at = datetime.utcnow()
        await self.engine.save(showtime)
        logging.info(f"Showtime updated: {showtime.id}")
        return showtime

    async def delete_showtime(self, showtime_id: str) -> dict:
        """Delete showtime by ID"""
        showtime = await self.get_showtime(showtime_id)
        await self.engine.delete(showtime)
        logging.info(f"Showtime deleted: {showtime_id}")
        return {"message": "Showtime deleted successfully"}
