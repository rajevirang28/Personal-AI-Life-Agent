from fastapi import FastAPI

# Import Database Base class and engine setup for ORM initialization
from app.database.database import Base, engine
# Import User model so SQLAlchemy registers it before table get created
from app.models.user import User

# Auto create all define database tables on application startup
Base.metadata.create_all(bind=engine)

# Initialize the main FastAPI application instance with metadata for Swagger docs
app = FastAPI(
    title="Personal AI Life & Productivity Agent",
    description="AI-powered personal productivity and life management platform",
    version="0.1.0"
)

# Root: Returns a basic welcome message to verify the API is running
@app.get("/")
def root():
    return{
        "message": "Personal AI Agent API is running"
    }

# About: Provides metadata about the application name, version and developer 
@app.get("/about")
def get_about():
    return{
        "name": "Personal AI Life & Productivity Agent",
        "version": "0.1.0",
        "developer": "Virang Raje"
    }

# Feature: Return a list of core functionalities offeref by the platform
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

# Health Check: Used by monitoring tools or load balancers to check service availability
@app.get("/health")
def health_check():
    return{
        "status": "healthy"
    }
