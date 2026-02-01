from datetime import datetime
from typing import Optional

from odmantic import Field, Model, ObjectId


class Showtime(Model):
    """
    Model representing a specific screening of a movie at a theater.
    """

    movie_id: ObjectId = Field(..., description="Reference to the Movie")
    theater_id: ObjectId = Field(..., description="Reference to the Theater")
    screen_id: ObjectId = Field(
        ..., description="Reference to the Screen within the Theater"
    )

    start_time: datetime = Field(..., description="When the show starts")
    end_time: datetime = Field(..., description="When the show ends")

    # Base price could be here, or in a detailed seat map structure
    base_price: float = Field(..., gt=0, description="Base ticket price for this show")

    is_active: bool = Field(default=True, description="Whether this showtime is valid")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"collection": "showtimes"}
