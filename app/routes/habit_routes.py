from fastapi import APIRouter, Depends, HTTPException, Query, Path, Response, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func, and_
from typing import Optional, List
from datetime import datetime, timedelta

from app.database import get_db
from app.models.habits import Habit
from app.models.habit_logs import HabitLog
from app.utils.auth import get_current_user, oauth2_scheme

from app.schemas.habit import HabitCreate, HabitUpdate
from app.schemas.habit_log import HabitLogCreate

habit_router = APIRouter()

def _habit_to_dict(h: Habit) -> dict:
    return {
        "id": h.id,
        "title": h.title,
        "description": h.description,
        "is_active": getattr(h, "is_active", True),
        "created_at": h.created_at,
        "updated_at": h.updated_at,
    }

def _log_to_dict(l: HabitLog) -> dict:
    return {
        "id": l.id,
        "habit_id": l.habit_id,
        "logged_at": l.logged_at,
        "title": getattr(l, "title", None),
        "description": getattr(l, "description", None),
    }

@habit_router.get("/habits", response_model=dict)
def list_habits(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    base_query = db.query(Habit).filter(Habit.user_id == current_user.id)
    if search:
        base_query = base_query.filter(Habit.title.ilike(f"%{search}%"))
    total = base_query.count()
    habits = base_query.offset(offset).limit(limit).all()
    items = [_habit_to_dict(h) for h in habits]
    return {"items": items, "total": total}

@habit_router.post("/habits", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_habit(
    habit_in: HabitCreate,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    habit = Habit(
        title=habit_in.title,
        description=habit_in.description,
        user_id=current_user.id,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return _habit_to_dict(habit)

@habit_router.get("/habits/{habit_id}", response_model=dict)
def get_habit(
    habit_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    habit = (
        db.query(Habit)
        
        .filter(and_(Habit.id == habit_id, Habit.user_id == current_user.id))
        .first()
    )
    if not habit:
        raise HTTPException(status_code=404, detail="Not found")

    # Calculate current streak (consecutive days with logs up to today)
    today = datetime.utcnow().date()
    streak = 0
    logs = (
        db.query(HabitLog)
        .filter(HabitLog.habit_id == habit.id)
        .order_by(HabitLog.logged_at.desc())
        .all()
    )
    expected_day = today
    for log in logs:
        log_day = log.logged_at.date() if isinstance(log.logged_at, datetime) else log.logged_at
        if log_day == expected_day:
            streak += 1
            expected_day -= timedelta(days=1)
        elif log_day < expected_day:
            break
    habit_dict = _habit_to_dict(habit)
    habit_dict["current_streak"] = streak
    return habit_dict

@habit_router.put("/habits/{habit_id}", response_model=dict)
def update_habit(
    habit_in: HabitUpdate,
    habit_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    habit = (
        db.query(Habit)
        .filter(and_(Habit.id == habit_id, Habit.user_id == current_user.id))
        .first()
    )
    if not habit:
        raise HTTPException(status_code=404, detail="Not found")
    if habit_in.title is not None:
        habit.title = habit_in.title
    if habit_in.description is not None:
        habit.description = habit_in.description
    if hasattr(habit_in, "is_active") and habit_in.is_active is not None:
        habit.is_active = habit_in.is_active
    habit.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(habit)
    return _habit_to_dict(habit)

@habit_router.delete("/habits/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(
    habit_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    habit = (
        db.query(Habit)
        .filter(and_(Habit.id == habit_id, Habit.user_id == current_user.id))
        .first()
    )
    if not habit:
        raise HTTPException(status_code=404, detail="Not found")
    # Delete associated logs first
    db.query(HabitLog).filter(HabitLog.habit_id == habit.id).delete()
    db.delete(habit)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@habit_router.post("/habits/{habit_id}/log", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_habit_log(
    log_in: HabitLogCreate,
    habit_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    habit = (
        db.query(Habit)
        .filter(and_(Habit.id == habit_id, Habit.user_id == current_user.id))
        .first()
    )
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    log = HabitLog(
        habit_id=habit.id,
        title=log_in.title,
        description=log_in.description,
        logged_at=log_in.logged_at or datetime.utcnow(),
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return _log_to_dict(log)

@habit_router.get("/habits/{habit_id}/logs", response_model=dict)
def list_habit_logs(
    habit_id: int = Path(...),
    limit: int = Query(20, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    habit = (
        db.query(Habit)
        .filter(and_(Habit.id == habit_id, Habit.user_id == current_user.id))
        .first()
    )
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    base_query = db.query(HabitLog).filter(HabitLog.habit_id == habit.id)
    total = base_query.count()
    logs = base_query.offset(offset).limit(limit).all()
    items = [_log_to_dict(l) for l in logs]
    return {"items": items, "total": total}

@habit_router.delete("/habits/{habit_id}/logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit_log(
    habit_id: int = Path(...),
    log_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    habit = (
        db.query(Habit)
        .filter(and_(Habit.id == habit_id, Habit.user_id == current_user.id))
        .first()
    )
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    log = (
        db.query(HabitLog)
        .filter(and_(HabitLog.id == log_id, HabitLog.habit_id == habit.id))
        .first()
    )
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(log)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
