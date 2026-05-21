from pydantic import BaseModel


# Schema for incoming event creation requests
class EventCreate(BaseModel):

    # Type of event triggered by user activity
    event_type: str

    # Additional event-related metadata
    metadata: dict