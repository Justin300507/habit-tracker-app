from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta
import uuid

from app.database import get_db
from app.utils.auth import (
    create_access_token,
    verify_password,
    get_password_hash,
    get_current_user,
    oauth2_scheme,
)

# OAuth2 scheme for token generation (used by clients when obtaining a token)
# Note: oauth2_scheme is imported from app.utils.auth to avoid redefining it here.

auth_router = APIRouter()

# ---------------------------------------------------------------------------
# Request / response schemas (inline as required)
# ---------------------------------------------------------------------------
class AuthRegisterRequest(BaseModel):
    email: EmailStr = Field(..., min_length=1)
    password: str = Field(..., min_length=8)

class AuthLoginRequest(BaseModel):
    email: EmailStr = Field(..., min_length=1)
    password: str = Field(..., min_length=8)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., min_length=1)

class PasswordResetConfirm(BaseModel):
    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)

# ---------------------------------------------------------------------------
# Helper: lazy import of models to avoid duplicate table registration
# ---------------------------------------------------------------------------
def _get_user_model():
    from app.models.users import User  # noqa: F401
    return User

def _get_password_reset_token_model():
    from app.models.password_reset_tokens import PasswordResetToken  # noqa: F401
    return PasswordResetToken

# ---------------------------------------------------------------------------
# Endpoint implementations
# ---------------------------------------------------------------------------
@auth_router.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(request: AuthRegisterRequest, db: Session = Depends(get_db)):
    User = _get_user_model()
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(request.password)
    new_user = User(email=request.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Placeholder: send verification email here
    return {"id": new_user.id, "email": new_user.email}

@auth_router.post("/auth/login", response_model=TokenResponse)
def login(request: AuthLoginRequest, db: Session = Depends(get_db)):
    User = _get_user_model()
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/auth/password-reset-request")
def password_reset_request(request: PasswordResetRequest, db: Session = Depends(get_db)):
    User = _get_user_model()
    PasswordResetToken = _get_password_reset_token_model()
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token_str = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=1)
    token_entry = PasswordResetToken(user_id=user.id, token=token_str, expires_at=expires_at)
    db.add(token_entry)
    db.commit()
    # Placeholder: send password reset email containing token_str
    return {"msg": "Password reset email sent"}

@auth_router.post("/auth/password-reset")
def password_reset(confirm: PasswordResetConfirm, db: Session = Depends(get_db)):
    PasswordResetToken = _get_password_reset_token_model()
    User = _get_user_model()
    token_obj = (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.token == confirm.token)
        .first()
    )
    if not token_obj:
        raise HTTPException(status_code=400, detail="Invalid token")
    if token_obj.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")
    user = db.query(User).filter(User.id == token_obj.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password_hash = get_password_hash(confirm.new_password)
    db.delete(token_obj)
    db.commit()
    return {"msg": "Password has been reset"}
