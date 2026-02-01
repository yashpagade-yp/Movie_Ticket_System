from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from odmantic import Field, Model, ObjectId


class SeatLayout(BaseModel):
    """
    Represents the physical layout of seats in a screen.
    Simplified as rows and columns or a list of seat labels.
    """

    rows: int = Field(..., description="Number of rows")
    columns: int = Field(..., description="Number of columns")
    seat_types: dict = Field(
        default_factory=dict,
        description="Mapping of seat labels to types e.g. {'A1': 'GOLD'}",
    )


class Screen(Model):
    """
    A specific screen/auditorium within a theater.
    """

    theater_id: ObjectId = Field(..., description="The theater this screen belongs to")
    name: str = Field(..., description="Screen name or number e.g. Screen 1")
    capacity: int = Field(..., description="Total seating capacity")
    layout: Optional[SeatLayout] = Field(
        default=None, description="Physical seat layout"
    )

    is_3d_enabled: bool = Field(default=False)
    is_imax: bool = Field(default=False)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"collection": "screens"}


class Theater(Model):
    """
    Model representing a physical Cinema/Theater.
    """

    owner_id: ObjectId = Field(
        ..., description="The User (Theater Owner) who owns this"
    )
    name: str = Field(..., min_length=2, max_length=100)
    location: str = Field(..., description="City or locality")
    address: str = Field(..., description="Full physical address")
    contact_number: Optional[str] = Field(default=None)

    is_active: bool = Field(default=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"collection": "theaters"}
