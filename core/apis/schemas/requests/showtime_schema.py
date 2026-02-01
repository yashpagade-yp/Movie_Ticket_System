from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from odmantic import ObjectId


class ShowtimeCreate(BaseModel):
    movie_id: str = Field(..., description="Movie ID (hex string)")
    theater_id: str = Field(..., description="Theater ID (hex string)")
    screen_id: str = Field(..., description="Screen ID (hex string)")
    start_time: datetime
    end_time: datetime
    base_price: float = Field(..., gt=0)


class ShowtimeUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    base_price: Optional[float] = None
    is_active: Optional[bool] = None
