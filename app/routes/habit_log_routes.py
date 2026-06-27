from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional, Dict

from app.database import get_db
from app.models.habits import Habit
from app.models.habit_logs import HabitLog
from app.schemas.habit_log import HabitLogCreate
from app.utils.auth import get_current_user

habit_log_router = APIRouter()


def _habit_log_to_dict(log: HabitLog) -> Dict:
    return {"id": log.id, "habit_id": log.habit_id, "date": str(log.date)}


@habit_log_router.post("/habits/{habit_id}/log", response_model=Dict, status_code=status.HTTP_201_CREATED)
def create_habit_log(
    habit_log_in: HabitLogCreate,
    habit_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    log = HabitLog(habit_id=habit_id, date=habit_log_in.date or datetime.utcnow().date())
    db.add(log)
    habit.streak = (habit.streak or 0) + 1
    habit.last_completed_date = datetime.utcnow().date()
    db.commit()
    db.refresh(log)
    return _habit_log_to_dict(log)


@habit_log_router.get("/habits/{habit_id}/logs", response_model=Dict)
def list_habit_logs(
    habit_id: int = Path(..., gt=0),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    query = db.query(HabitLog).filter(HabitLog.habit_id == habit_id)
    if start_date:
        query = query.filter(HabitLog.date >= start_date)
    if end_date:
        query = query.filter(HabitLog.date <= end_date)
    total = query.count()
    logs = query.order_by(HabitLog.date.desc()).offset(offset).limit(limit).all()
    return {"items": [_habit_log_to_dict(l) for l in logs], "total": total}


@habit_log_router.delete("/habits/{habit_id}/logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit_log(
    habit_id: int = Path(..., gt=0),
    log_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    log = db.query(HabitLog).filter(HabitLog.id == log_id, HabitLog.habit_id == habit_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(log)
    db.commit()
    return None
