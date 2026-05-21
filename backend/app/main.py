from fastapi import FastAPI
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware

from slowapi.middleware import SlowAPIMiddleware

from app.api.auth import router as auth_router
from app.api.events import router as events_router
from app.api.analytics import router as analytics_router

from app.websocket.events_ws import router as websocket_router

from app.core.auth import get_current_user
from app.core.limiter import limiter
from app.models.alert import Alert
from app.core.exceptions import (
    global_exception_handler
)
from app.api.alerts import router as alerts_router
from app.core.database import engine
from app.core.database import Base
from app.api.reports import router as reports_router
# Initialize FastAPI application
app = FastAPI(
    title="Real-Time Analytics Platform"
)

app.add_exception_handler(
    Exception,
    global_exception_handler
)
# Configure CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Attach rate limiter to application state
app.state.limiter = limiter


# Add global rate limiting middleware
app.add_middleware(SlowAPIMiddleware)


# Register API and WebSocket routers
app.include_router(auth_router)
app.include_router(events_router)
app.include_router(websocket_router)
app.include_router(analytics_router)
app.include_router(alerts_router)
app.include_router(reports_router)
# Health check endpoint
@app.get("/")
async def root():

    return {
        "message": "Analytics Platform Running"
    }


# Example protected route using JWT authentication
@app.get("/protected")
async def protected_route(
    current_user: str = Depends(get_current_user)
):

    return {
        "message": "Protected route accessed",
        "user": current_user
    }
@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )