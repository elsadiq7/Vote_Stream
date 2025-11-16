# -----------------------------
# Import necessary libraries
# -----------------------------
from math import e
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
import psycopg2
from .config import settings
# -----------------------------
# Database Configuration
# -----------------------------
# Define the URL for the PostgreSQL database connection
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# -----------------------------
# Engine Creation
# -----------------------------
# The engine is the core interface to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# -----------------------------
# Session Configuration
# -----------------------------
# Create a session factory for managing database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -----------------------------
# Base Class for ORM Models
# -----------------------------
# This base class will be inherited by all database models
Base = declarative_base()

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                 password='postgres', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)