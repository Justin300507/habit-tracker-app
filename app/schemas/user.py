from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class UserCreate(BaseModel):
    username: str = Field(min_length=1)
    email: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    password: str = Field(min_length=1)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=1)
    email: Optional[str] = Field(default=None, min_length=1)
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    password: Optional[str] = Field(default=None, min_length=1)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)

class UserRead(BaseModel):
    id: int
    username: str
    email: str
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)
