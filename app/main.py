# ===========================================================
# Imports
# ===========================================================
from ssl import create_default_context  # For secure SSL connections (not used here, but imported)
from turtle import mode, title
from fastapi import FastAPI, Response, status, HTTPException
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from fastapi.params import Depends
from . import models,scehmas
from .database import engine , get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)  # Create database tables

# ===========================================================
# FastAPI App Initialization
# ===========================================================
app = FastAPI(title="FastAPI Posts API", version="1.0")



# ===========================================================
# Routes (Endpoints)
# ===========================================================

@app.get("/")
def root():
    """Root endpoint to verify the API is working."""
    return {"message": "Welcome to the FastAPI Posts API"}


# -----------------------------------------------------------
# Get all posts
# -----------------------------------------------------------

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return db.query(models.Posts).all()


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    """
    Retrieve all posts from the database.
    """
    # cursor.execute("SELECT * FROM posts;")
    # posts = cursor.fetchall()
    posts=db.query(models.Posts).all()
    return {"data": posts}


# -----------------------------------------------------------
# Create a new post
# -----------------------------------------------------------
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: scehmas.Post,db: Session = Depends(get_db)):
    """
    Create a new post.
    - Validates input using the Post model.
    - Inserts into the PostgreSQL database.
    """
    # cursor.execute(
    #     """
    #     INSERT INTO posts (title, content, published)
    #     VALUES (%s, %s, %s)
    #     RETURNING *;
    #     """,
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post=models.Posts(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


# -----------------------------------------------------------
# Retrieve a single post by ID
# -----------------------------------------------------------
@app.get("/posts/{id}")
def get_post(id: int,db: Session = Depends(get_db)):
    """
    Retrieve a specific post by ID.
    - Returns HTTP 404 if not found.
    """
    # cursor.execute("SELECT * FROM posts WHERE id = %s;", (str(id),))
    # post = cursor.fetchone()
    post=db.query(models.Posts).filter(models.Posts.id==id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )

    return {"post_detail": post}


# -----------------------------------------------------------
# Delete a post by ID
# -----------------------------------------------------------
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    """
    Delete a post by ID.
    - Returns HTTP 404 if the post doesn't exist.
    - Returns 204 (No Content) upon success.
    """
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post= deleted_post=db.query(models.Posts).filter(models.Posts.id==id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )
    post.delete(synchronize_session=False)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# -----------------------------------------------------------
# Update an existing post
# -----------------------------------------------------------
@app.put("/posts/{id}")
def update_post(id: int, updated_post: scehmas.Post, db: Session = Depends(get_db)):
    """
    Update a post by its ID.
    - Validates input using the Post model.
    - Returns HTTP 404 if the post doesn't exist.
    """
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )

    # ✅ Exclude fields that shouldn't be updated
    data = updated_post.model_dump(exclude_unset=True, exclude={"id", "created_at"})
    post_query.update(data, synchronize_session=False)
    db.commit()

    return {"data": post_query.first()}
