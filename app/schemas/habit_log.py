from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class HabitLogCreate(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    logged_at: Optional[datetime] = None  # defaults to now if not provided

class HabitLogUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    logged_at: Optional[datetime] = None

class HabitLogResponse(BaseModel):
    id: int
    habit_id: int
    title: str
    description: Optional[str] = None
    logged_at: Optional[datetime] = None
    streak: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
