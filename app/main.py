# ===========================================================
# Imports
# ===========================================================
from ssl import create_default_context  # For secure SSL connections (not used here, but imported)
from turtle import mode, title
from fastapi import FastAPI,APIRouter, Response, status, HTTPException
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from fastapi.params import Depends
from . import models, schemas,utils
from .database import engine , get_db
from .routers import post,user,auth

models.Base.metadata.create_all(bind=engine)
  # Create database tables
# ===========================================================
# FastAPI App Initialization
# ===========================================================
app = FastAPI(title="FastAPI Posts API", version="1.0")



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
# ===========================================================
# Routes (Endpoints)
# ===========================================================

@app.get("/")
def root():
    """Root endpoint to verify the API is working."""
    return {"message": "Welcome to the FastAPI Posts API"}




       