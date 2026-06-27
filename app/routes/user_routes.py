from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.auth import get_current_user, oauth2_scheme, get_password_hash
from app.schemas.user import UserRead, UserUpdate

# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

user_router = APIRouter()

@user_router.get("/users/me", response_model=UserRead)
def read_current_user(current_user: "User" = Depends(get_current_user)):
    """Return the profile of the authenticated user."""
    return current_user

@user_router.put("/users/me", response_model=UserRead, status_code=status.HTTP_200_OK)
def update_current_user(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    """Update the authenticated user's profile.

    Only fields provided in the request body are updated.
    """
    if user_in.username is not None:
        current_user.username = user_in.username
    if user_in.email is not None:
        current_user.email = user_in.email
    if user_in.title is not None:
        current_user.title = user_in.title
    if user_in.description is not None:
        current_user.description = user_in.description
    if user_in.password is not None:
        # Hash the new password before storing it
        current_user.password_hash = get_password_hash(user_in.password)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
