from sqlalchemy import Column, Integer, String

from app.database.database import Base

# Define the User database model inheriting from SQLAlchemy's Base class
class User(Base):
    # Specify the name of the database table
    __tablename__ = "users"

    # Primary key column
    id = Column(Integer, primary_key=True, index=True)
    # User's full name
    name = Column(String(100), nullable=False)
    # User's email
    email = Column(String(150), unique=True, nullable=False, index=True)