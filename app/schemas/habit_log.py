from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


class HabitLogCreate(BaseModel):
    date: Optional[date] = None  # defaults to today if not provided
    model_config = ConfigDict(from_attributes=True)
