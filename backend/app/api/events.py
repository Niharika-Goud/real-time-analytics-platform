from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.future import select

from app.websocket.manager import manager
from app.core.dependencies import get_db
from app.core.auth import get_current_user

from app.models.event import Event
from app.models.alert import Alert

from app.schemas.event import EventCreate


# Event ingestion router for tracking user activity
router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


# Create a new event and broadcast it in real time
@router.post("/")
async def create_event(
    payload: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    # Create new event entry
    event = Event(
    event_type=payload.event_type,
    user_email=current_user.email,
    event_metadata=payload.metadata
)

    try:

        # Store event in database
        db.add(event)

        await db.commit()

        await db.refresh(event)

        # Count total events
        total_events_result = await db.execute(
            select(func.count(Event.id))
        )

        total_events = total_events_result.scalar()

        # Trigger alert if threshold exceeded
        if total_events > 5:

            alert = Alert(
                message="High event volume detected"
            )

            db.add(alert)

            await db.commit()

            # Broadcast alert to all websocket clients
            await manager.broadcast({
                "type": "alert",
                "message": alert.message
            })

    except Exception:

        # Rollback database transaction if error occurs
        await db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )

    # Broadcast live event to all connected websocket clients
    await manager.broadcast({
        "event_type": event.event_type,
        "user": event.user_email
    })

    return {
        "message": "Event created",
        "event_id": event.id
    }