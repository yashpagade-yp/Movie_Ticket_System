from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


class SeatLayoutSchema(BaseModel):
    rows: int = Field(..., gt=0)
    columns: int = Field(..., gt=0)
    seat_types: Dict[str, str] = {}


class ScreenCreate(BaseModel):
    name: str = Field(..., min_length=1)
    capacity: int = Field(..., gt=0)
    layout: Optional[SeatLayoutSchema] = None
    is_3d_enabled: bool = False
    is_imax: bool = False


class TheaterCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    location: str
    address: str
    contact_number: Optional[str] = None


class TheaterUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None
    is_active: Optional[bool] = None
