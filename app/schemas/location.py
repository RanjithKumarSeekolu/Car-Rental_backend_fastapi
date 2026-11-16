from pydantic import Field, field_validator
from app.schemas.base import CamelModel


class Coordinates(CamelModel):
  lat: float = Field(ge=-90, le=90)
  lng: float = Field(ge=-180, le=180)


class Bounds(CamelModel):
  north: float
  south: float
  east: float
  west: float


class Location(CamelModel):
  id: str
  name: str
  state: str = ""
  country: str = "IN"
  center: Coordinates
  bounds: Bounds | None = None
  is_active: bool = True
  sort_order: int = 99
  type: str = "city"


class LocationResponse(CamelModel):
  success: bool = True
  location: Location


class LocationListResponse(CamelModel):
  success: bool = True
  locations: list[Location]

class LocationCreate(CamelModel):
  id: str | None = None
  name: str = Field(min_length=1)
  state: str = ""
  country: str = "IN"
  center: Coordinates
  bounds: Bounds | None = None
  is_active: bool = True
  sort_order: int = 99

class LocationUpdate(CamelModel):
  name: str | None = Field(default=None, min_length=1)
  state: str | None = None
  country: str | None = None
  center: Coordinates | None = None
  bounds: Bounds | None = None      # null allowed: clears the bounds
  is_active: bool | None = None
  sort_order: int | None = None

  @field_validator("name", "state", "country", "center", "is_active", "sort_order")
  @classmethod
  def reject_null(cls, value):
    if value is None:
      raise ValueError("cannot be null")
    return value