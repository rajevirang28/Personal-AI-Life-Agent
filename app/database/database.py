import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from a .env file into os.environ
load_dotenv()

# Retrieve the database connection string from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine to manage database connections
engine = create_engine(DATABASE_URL)

# Create a configured "SessionLocal" class for instantiating database sessions
SessionLocal = sessionmaker(
    autocommit = False, # Prevent auto-committing transactions
    autoflush = False, # Prevent auto-flushing pending changes to the database before queries
    bind = engine # Bind this session factory to our database engine
)

# Define the base class for mapping python classes to database tables
Base = declarative_base()

# Dependency function to manage database session lifecycle per request
def get_db():
    db = SessionLocal() # Open a new database session

    try:
        yield db # Yield the session to the caller
    finally:
        db.close() # Ensure the session is closed after the request completes