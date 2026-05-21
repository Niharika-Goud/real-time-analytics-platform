from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.event import Event

from app.core.cache import redis_client
from app.core.limiter import limiter

import json


# Analytics router for aggregated platform insights
router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


# Protected analytics endpoint with rate limiting
@router.get("/stats")
@limiter.limit("5/minute")
async def get_stats(

    request: Request,

    db: AsyncSession = Depends(get_db)
):

    # Check if analytics data exists in Redis cache
    try:

        cached_stats = redis_client.get(
            "analytics_stats"
        )

    except Exception:

        cached_stats = None

    if cached_stats:

        return json.loads(cached_stats)


    # Count total events generated in the platform
    total_events_result = await db.execute(
        select(func.count(Event.id))
    )

    total_events = total_events_result.scalar()


    # Count unique users generating events
    unique_users_result = await db.execute(
        select(func.count(func.distinct(Event.user_email)))
    )

    unique_users = unique_users_result.scalar()


    # Fetch most frequent event type
    top_event_result = await db.execute(
        select(
            Event.event_type,
            func.count(Event.event_type)
        )
        .group_by(Event.event_type)
        .order_by(func.count(Event.event_type).desc())
        .limit(1)
    )

    top_event = top_event_result.first()


    # Final analytics response
    response = {
        "total_events": total_events,
        "unique_users": unique_users,
        "top_event": top_event[0] if top_event else None
    }


    # Store analytics response in Redis cache for 60 seconds
    redis_client.setex(
        "analytics_stats",
        60,
        json.dumps(response)
    )

    return response