# ===========================================================
# Imports
# ===========================================================
from ssl import create_default_context  # For secure SSL connections (not used here, but imported)
from turtle import mode, title
from fastapi import FastAPI
from random import randrange
from fastapi.middleware.cors import CORSMiddleware

from app.outh2 import SECRET_KEY

from . import models
from .database import engine , get_db
from .routers import post,user,auth,vote
from .config import Settings 

settings=Settings()

#models.Base.metadata.create_all(bind=engine)
  # Create database tables
# ===========================================================
# FastAPI App Initialization
# ===========================================================
app = FastAPI(title="FastAPI Posts API", version="1.0")

origins=[
    "*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
# ===========================================================
# Routes (Endpoints)
# ===========================================================

@app.get("/")
def root():
    """Root endpoint to verify the API is working."""
    return {"message": "Welcome to the FastAPI Posts API"}




       