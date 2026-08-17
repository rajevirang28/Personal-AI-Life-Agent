from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class MemoryCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200
    )

    content: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    memory_type: str = Field(
        default="note",
        pattern="^(note|goal|preference|idea|important)$"
    )

class MemoryUpdate(BaseModel):

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    content: str | None = Field(
        default=None,
        min_length=1,
        max_length=5000
    )

    memory_type: str | None = Field(
        default=None,
        pattern="^(note|goal|preference|idea|important)$"
    )

class MemoryResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    user_id: int
    title: str
    content: str
    memory_type: str
    created_at: datetime
    updated_at: datetime