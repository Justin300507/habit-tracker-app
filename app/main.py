from fastapi import FastAPI

# Router imports
from app.routes.habit_log_routes import habit_log_router
from app.routes.user_routes import user_router
from app.routes.dashboard_routes import dashboard_router
from app.routes.auth_routes import auth_router
from app.routes.habit_routes import habit_router

# Model imports (ensure all tables are registered)
from app.models.users import *  # noqa: F401
from app.models.habits import *  # noqa: F401
from app.models.habit_logs import *  # noqa: F401
from app.models.password_reset_tokens import *  # noqa: F401

# Database imports
from app.database import Base, engine

app = FastAPI()

# CORS (required for frontend access)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint (required for deployment health checks)
@app.get("/health")
def health():
    return {"status": "ok"}

# Create all tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(habit_log_router)
app.include_router(user_router)
app.include_router(dashboard_router)
app.include_router(auth_router)
app.include_router(habit_router)
