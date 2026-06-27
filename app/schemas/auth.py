from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class AuthCreate(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)

class AuthUpdate(BaseModel):
    email: Optional[str] = Field(default=None, min_length=1)
    password: Optional[str] = Field(default=None, min_length=1)

class AuthResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)

class RegisterRequest(BaseModel):
    username: str = Field(min_length=1)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
