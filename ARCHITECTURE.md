# Architecture — Habit Tracker App

## ER Diagram

```
┌─────────────────────┐
│ HabitLog            │
├─────────────────────┤
│ id         Integer ││
│ habit_id   Integer ││
│ date       Date    ││
│ created_at DateTime││
└─────────────────────┘

┌─────────────────────┐
│ Habit               │
├─────────────────────┤
│ id         Integer ││
│ user_id    Integer ││
│ name       String  ││
│ description String  ││
│ created_at DateTime││
│ is_active  Boolean ││
│ streak     Integer ││
│ last_completed_date D│
└─────────────────────┘

┌─────────────────────┐
│ PasswordResetToken  │
├─────────────────────┤
│ id         Integer ││
│ user_id    Integer ││
│ token      String  ││
│ expires_at DateTime││
│ created_at DateTime││
└─────────────────────┘

┌─────────────────────┐
│ User                │
├─────────────────────┤
│ id         Integer ││
│ email      String  ││
│ password_hash String │
│ created_at DateTime││
│ is_active  Boolean ││
└─────────────────────┘

```

## Backend Architecture

```
FastAPI Application
├── Routing Layer (app/routes/)     → HTTP request handling
├── Service Layer (app/services/)   → Business logic
├── Model Layer (app/models/)       → Database ORM (SQLAlchemy)
├── Schema Layer (app/schemas/)     → Validation (Pydantic v2)
└── Database (app/database.py)      → Session management (SQLite)
```

## Design Patterns

- **Repository pattern**: services own DB queries, routes own HTTP logic
- **Dependency injection**: `get_db` session injected via FastAPI `Depends()`
- **Schema separation**: ORM models never exposed directly; Pydantic schemas serialize responses
- **JWT auth**: Bearer tokens validated via `oauth2_scheme` dependency
