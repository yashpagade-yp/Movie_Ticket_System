from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from odmantic import ObjectId

from core.models.theater_model import Theater, Screen, SeatLayout
from core.apis.schemas.requests.theater_schema import (
    TheaterCreate,
    TheaterUpdate,
    ScreenCreate,
    SeatLayoutSchema,
)
from core.database.database import get_engine
from commons.loggers import logger

logging = logger(__name__)


class TheaterController:
    @property
    def engine(self):
        return get_engine()

    # --- Theater Operations ---

    async def create_theater(self, theater_data: TheaterCreate, owner_id: str):
        """Create a new theater"""
        theater = Theater(owner_id=ObjectId(owner_id), **theater_data.model_dump())
        await self.engine.save(theater)
        logging.info(f"Theater created: {theater.name}")

        # Convert to dict for proper serialization
        theater_dict = theater.model_dump()
        theater_dict["id"] = str(theater.id)
        theater_dict["owner_id"] = str(theater.owner_id)
        return theater_dict

    async def get_theater(self, theater_id: str):
        """Get theater by ID"""
        try:
            theater = await self.engine.find_one(
                Theater, Theater.id == ObjectId(theater_id)
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Theater ID"
            )

        if not theater:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Theater not found"
            )

        # Convert to dict for proper serialization
        theater_dict = theater.model_dump()
        theater_dict["id"] = str(theater.id)
        theater_dict["owner_id"] = str(theater.owner_id)
        return theater_dict

    async def get_all_theaters(self, location: Optional[str] = None):
        """List all theaters with optional location filter"""
        if location:
            theaters = await self.engine.find(Theater, Theater.location == location)
        else:
            theaters = await self.engine.find(Theater)

        # Convert to list of dicts for proper serialization
        result = []
        for theater in theaters:
            theater_dict = theater.model_dump()
            theater_dict["id"] = str(theater.id)
            theater_dict["owner_id"] = str(theater.owner_id)
            result.append(theater_dict)
        return result

    async def update_theater(self, theater_id: str, update_data: TheaterUpdate):
        """Update theater details"""
        theater_dict = await self.get_theater(theater_id)

        # Get the actual theater object
        theater = await self.engine.find_one(
            Theater, Theater.id == ObjectId(theater_id)
        )

        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(theater, field, value)

        theater.updated_at = datetime.utcnow()
        await self.engine.save(theater)
        logging.info(f"Theater updated: {theater.name}")

        # Convert to dict for proper serialization
        theater_dict = theater.model_dump()
        theater_dict["id"] = str(theater.id)
        theater_dict["owner_id"] = str(theater.owner_id)
        return theater_dict

    async def delete_theater(self, theater_id: str) -> dict:
        """Delete theater by ID"""
        theater = await self.get_theater(theater_id)
        # Also delete associated screens
        screens = await self.engine.find(Screen, Screen.theater_id == theater.id)
        for screen in screens:
            await self.engine.delete(screen)

        await self.engine.delete(theater)
        logging.info(f"Theater deleted: {theater.name}")
        return {"message": "Theater and associated screens deleted successfully"}

    # --- Screen Operations ---

    async def add_screen(self, theater_id: str, screen_data: ScreenCreate) -> Screen:
        """Add a screen to a theater"""
        theater = await self.get_theater(theater_id)

        layout = None
        if screen_data.layout:
            layout = SeatLayout(
                rows=screen_data.layout.rows,
                columns=screen_data.layout.columns,
                seat_types=screen_data.layout.seat_types,
            )

        screen = Screen(
            theater_id=theater.id,
            name=screen_data.name,
            capacity=screen_data.capacity,
            layout=layout,
            is_3d_enabled=screen_data.is_3d_enabled,
            is_imax=screen_data.is_imax,
        )
        await self.engine.save(screen)
        logging.info(f"Screen {screen.name} added to theater {theater.name}")
        return screen

    async def get_theater_screens(self, theater_id: str) -> List[Screen]:
        """Get all screens for a specific theater"""
        theater = await self.get_theater(theater_id)
        return await self.engine.find(Screen, Screen.theater_id == theater.id)

    async def get_screen(self, screen_id: str) -> Screen:
        """Get screen by ID"""
        try:
            screen = await self.engine.find_one(
                Screen, Screen.id == ObjectId(screen_id)
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Screen ID"
            )

        if not screen:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Screen not found"
            )
        return screen

    async def delete_screen(self, screen_id: str) -> dict:
        """Delete screen by ID"""
        screen = await self.get_screen(screen_id)
        await self.engine.delete(screen)
        logging.info(f"Screen deleted: {screen.name}")
        return {"message": "Screen deleted successfully"}
