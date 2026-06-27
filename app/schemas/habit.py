from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class HabitCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class HabitUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)

class HabitResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool
    streak: int = 0
    model_config = ConfigDict(from_attributes=True)
