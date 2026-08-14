from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable = False
    )

    title = Column(
        String(200),
        nullable = False
    )

    description = Column(
        Text,
        nullable = True
    )

    priority = Column(
        String(20),
        default = "medium",
        nullable = False
    )

    status = Column(
        String(20),
        default = "pending",
        nullable = False
    )

    due_date = Column(
        Date,
        nullable = True
    )

    created_at = Column(
        DateTime,
        server_default = func.now(),
        nullable = False
    )

    updated_at = Column(
        DateTime,
        server_default = func.now(),
        onupdate = func.now(),
        nullable = False
    )