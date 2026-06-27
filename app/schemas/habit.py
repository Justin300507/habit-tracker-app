from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class HabitCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)

    model_config = ConfigDict(from_attributes=True)

class HabitUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class HabitResponse(BaseModel):
    id: int
    title: str = Field(..., min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
