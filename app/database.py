# -----------------------------
# Import necessary libraries
# -----------------------------
from math import e
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -----------------------------
# Database Configuration
# -----------------------------
# Define the URL for the PostgreSQL database connection
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapi"

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
