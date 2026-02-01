from datetime import datetime
from enum import Enum
from typing import List, Optional

from odmantic import Field, Model


class MovieStatus(str, Enum):
    COMING_SOON = "COMING_SOON"
    NOW_SHOWING = "NOW_SHOWING"
    PAST = "PAST"


class Movie(Model):
    """
    Model representing a Movie.
    """

    title: str = Field(..., min_length=1, max_length=200, description="Movie title")
    description: str = Field(..., description="Short synopsis of the movie")
    language: str = Field(..., description="Audio language of the movie")
    genres: List[str] = Field(
        default_factory=list, description="List of genres e.g. Action, Drama"
    )
    duration_minutes: int = Field(..., gt=0, description="Duration in minutes")
    release_date: datetime = Field(..., description="Release date")
    poster_url: Optional[str] = Field(default=None, description="URL to movie poster")
    trailer_url: Optional[str] = Field(default=None, description="URL to trailer")

    status: MovieStatus = Field(
        default=MovieStatus.COMING_SOON, description="Current screening status"
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"collection": "movies"}
