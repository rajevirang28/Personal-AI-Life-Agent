from fastapi import FastAPI

from app.database.database import Base, engine

from app.models.user import User
from app.models.task import Task
from app.models.memory import Memory

from app.api.tasks import router as task_router
from app.api.auth import router as auth_router
from app.api.memory import router as memory_router
from app.api.chat import router as chat_router

Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="Personal AI Life & Productivity Agent",
    description="AI-powered personal productivity and life management platform",
    version="0.3.0"
)

app.include_router(auth_router)

app.include_router(task_router)

app.include_router(memory_router)

app.include_router(chat_router)

@app.get("/")
def root():
    return{
        "message": "Personal AI Agent API is running"
    }

@app.get("/health")
def health_check():
    return{
        "status": "healthy"
    }

@app.get("/about")
def get_about():
    return{
        "name": "Personal AI Life & Productivity Agent",
        "version": "0.3.0",
        "developer": "Virang Raje"
    }

@app.get("/features")
def get_features():
    return{
        "features": [
            "Task Management",
            "AI Assistant",
            "DSA Tracker",
            "Notes",
            "Document Search"
        ]
    }