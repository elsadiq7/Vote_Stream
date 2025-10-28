# ===========================================================
# Imports
# ===========================================================
from ssl import create_default_context  # For secure SSL connections (not used here, but imported)
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


# ===========================================================
# Sample in-memory data (for reference/testing)
# ===========================================================
my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2},
]


# ===========================================================
# FastAPI App Initialization
# ===========================================================
app = FastAPI(title="FastAPI Posts API", version="1.0")


# ===========================================================
# Database Connection (PostgreSQL)
# ===========================================================
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="postgres",
            cursor_factory=RealDictCursor,  # Return rows as dicts
        )
        cursor = conn.cursor()
        print("✅ Database connection was successful!")
        break
    except Exception as error:
        print("❌ Error while connecting to database:", error)
        time.sleep(2)  # Wait and retry every 2 seconds


# ===========================================================
# Pydantic Model - Request Validation Schema
# ===========================================================
class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True
    created_at: Optional[str] = None


# ===========================================================
# Helper Functions
# ===========================================================
def find_post(id: int):
    """Return a post by its ID (from in-memory data)."""
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id: int):
    """Return the index of a post by its ID (from in-memory data)."""
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


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
@app.get("/posts")
def get_posts():
    """
    Retrieve all posts from the database.
    """
    cursor.execute("SELECT * FROM posts;")
    posts = cursor.fetchall()
    return {"data": posts}


# -----------------------------------------------------------
# Create a new post
# -----------------------------------------------------------
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    """
    Create a new post.
    - Validates input using the Post model.
    - Inserts into the PostgreSQL database.
    """
    cursor.execute(
        """
        INSERT INTO posts (title, content, published)
        VALUES (%s, %s, %s)
        RETURNING *;
        """,
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


# -----------------------------------------------------------
# Retrieve a single post by ID
# -----------------------------------------------------------
@app.get("/posts/{id}")
def get_post(id: int):
    """
    Retrieve a specific post by ID.
    - Returns HTTP 404 if not found.
    """
    cursor.execute("SELECT * FROM posts WHERE id = %s;", (str(id),))
    post = cursor.fetchone()

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
def delete_post(id: int):
    """
    Delete a post by ID.
    - Returns HTTP 404 if the post doesn't exist.
    - Returns 204 (No Content) upon success.
    """
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# -----------------------------------------------------------
# Update an existing post
# -----------------------------------------------------------
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    """
    Update a post by its ID.
    - Validates input using the Post model.
    - Returns HTTP 404 if the post doesn't exist.
    """
    cursor.execute(
        """
        UPDATE posts
        SET title = %s, content = %s, published = %s
        WHERE id = %s
        RETURNING *;
        """,
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )

    return {"data": updated_post}
