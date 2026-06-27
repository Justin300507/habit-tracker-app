from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
from collections import defaultdict

from app.database import get_db
from app.models.habits import Habit
from app.models.habit_logs import HabitLog
from app.models.users import User
from app.utils.auth import get_current_user

dashboard_router = APIRouter()


@dashboard_router.get("/dashboard/weekly")
def get_weekly_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habits = db.query(Habit).filter(Habit.user_id == current_user.id).all()
    if not habits:
        return {"items": [], "total": 0}

    today = datetime.utcnow().date()
    start_date = today - timedelta(days=6)
    habit_ids = [h.id for h in habits]

    logs = db.query(HabitLog).filter(
        HabitLog.habit_id.in_(habit_ids),
        HabitLog.date >= start_date
    ).all()

    logs_by_habit = defaultdict(set)
    for log in logs:
        logs_by_habit[log.habit_id].add(log.date)

    result = []
    for habit in habits:
        dates = logs_by_habit.get(habit.id, set())
        weekly_completion = round(len(dates) / 7 * 100, 2)
        streak = 0
        for i in range(7):
            if (today - timedelta(days=i)) in dates:
                streak += 1
            else:
                break
        result.append({
            "habit_id": habit.id,
            "name": habit.name,
            "weekly_completion": weekly_completion,
            "streak": streak,
        })

    return {"items": result, "total": len(result)}
