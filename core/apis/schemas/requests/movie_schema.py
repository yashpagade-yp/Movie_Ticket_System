from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime
from core.models.movie_model import MovieStatus


class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str
    language: str
    genres: List[str] = []
    duration_minutes: int = Field(..., gt=0)
    release_date: datetime
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    status: MovieStatus = MovieStatus.COMING_SOON


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    genres: Optional[List[str]] = None
    duration_minutes: Optional[int] = None
    release_date: Optional[datetime] = None
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    status: Optional[MovieStatus] = None
