from fastapi import APIRouter, Depends, HTTPException, Query, Path, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.models.habits import Habit
from app.models.habit_logs import HabitLog
from app.utils.auth import get_current_user
from app.schemas.habit import HabitCreate, HabitUpdate
from app.schemas.habit_log import HabitLogCreate

habit_router = APIRouter()


def _habit_to_dict(h: Habit) -> dict:
    return {
        "id": h.id,
        "name": h.name,
        "description": h.description,
        "is_active": h.is_active,
        "streak": h.streak or 0,
        "created_at": h.created_at,
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
    current_user=Depends(get_current_user),
):
    base_query = db.query(Habit).filter(Habit.user_id == current_user.id)
    if search:
        base_query = base_query.filter(Habit.name.ilike(f"%{search}%"))
    total = base_query.count()
    habits = base_query.offset(offset).limit(limit).all()
    return {"items": [_habit_to_dict(h) for h in habits], "total": total}


@habit_router.post("/habits", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_habit(
    habit_in: HabitCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    habit = Habit(
        name=habit_in.name,
        description=habit_in.description,
        user_id=current_user.id,
        is_active=True,
        streak=0,
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return _habit_to_dict(habit)


@habit_router.get("/habits/{habit_id}", response_model=dict)
def get_habit(
    habit_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    habit = db.query(Habit).filter(and_(Habit.id == habit_id, Habit.user_id == current_user.id)).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Not found")
    today = datetime.utcnow().date()
    logs = db.query(HabitLog).filter(HabitLog.habit_id == habit.id).order_by(HabitLog.logged_at.desc()).all()
    streak = 0
    expected = today
    for log in logs:
        log_day = log.logged_at.date() if isinstance(log.logged_at, datetime) else log.logged_at
        if log_day == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif log_day < expected:
            break
    result = _habit_to_dict(habit)
    result["current_streak"] = streak
    return result


@habit_router.put("/habits/{habit_id}", response_model=dict)
def update_habit(
    habit_in: HabitUpdate,
    habit_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    habit = db.query(Habit).filter(and_(Habit.id == habit_id, Habit.user_id == current_user.id)).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Not found")
    if habit_in.name is not None:
        habit.name = habit_in.name
    if habit_in.description is not None:
        habit.description = habit_in.description
    if habit_in.is_active is not None:
        habit.is_active = habit_in.is_active
    db.commit()
    db.refresh(habit)
    return _habit_to_dict(habit)


@habit_router.delete("/habits/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(
    habit_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    habit = db.query(Habit).filter(and_(Habit.id == habit_id, Habit.user_id == current_user.id)).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Not found")
    db.query(HabitLog).filter(HabitLog.habit_id == habit.id).delete()
    db.delete(habit)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@habit_router.post("/habits/{habit_id}/log", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_habit_log(
    log_in: HabitLogCreate,
    habit_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    habit = db.query(Habit).filter(and_(Habit.id == habit_id, Habit.user_id == current_user.id)).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    log = HabitLog(
        habit_id=habit.id,
        title=log_in.title,
        description=log_in.description,
        logged_at=log_in.logged_at or datetime.utcnow(),
    )
    db.add(log)
    habit.streak = (habit.streak or 0) + 1
    habit.last_completed_date = datetime.utcnow().date()
    db.commit()
    db.refresh(log)
    return _log_to_dict(log)


@habit_router.get("/habits/{habit_id}/logs", response_model=dict)
def list_habit_logs(
    habit_id: int = Path(...),
    limit: int = Query(20, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    habit = db.query(Habit).filter(and_(Habit.id == habit_id, Habit.user_id == current_user.id)).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    total = db.query(HabitLog).filter(HabitLog.habit_id == habit.id).count()
    logs = db.query(HabitLog).filter(HabitLog.habit_id == habit.id).offset(offset).limit(limit).all()
    return {"items": [_log_to_dict(l) for l in logs], "total": total}


@habit_router.delete("/habits/{habit_id}/logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit_log(
    habit_id: int = Path(...),
    log_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    habit = db.query(Habit).filter(and_(Habit.id == habit_id, Habit.user_id == current_user.id)).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    log = db.query(HabitLog).filter(and_(HabitLog.id == log_id, HabitLog.habit_id == habit.id)).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(log)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
