from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        min_length = 1,
        max_length = 200
    )

    description: str | None = None

    priority: str = Field(
        default = "medium",
        pattern="^(low|medium|high)$"
    )

    due_date: date | None = None

class TaskUpdate(BaseModel):
    title: str | None = Field(
        default = None,
        min_length=1,
        max_length=200
    )

    description: str | None = None

    priority: str | None = Field(
        default=None,
        pattern="^(low|medium|high)$"
    )

    status: str | None = Field(
        default=None,
        pattern="^(pending|in_progress|completed)$"
    )

    due_date: date | None = None

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    description: str | None
    priority: str
    status: str
    due_date: date | None
    created_at: datetime
    updated_at: datetime
