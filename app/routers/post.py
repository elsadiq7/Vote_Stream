
from app import outh2
from .. import models,schemas,outh2
from fastapi import  Response, status, HTTPException,Depends,APIRouter
from typing import List
from sqlalchemy.orm import Session
from ..database import   get_db
router=APIRouter(

    prefix="/posts",
    tags=["Posts"]
    
)
 
# -----------------------------------------------------------
# Get all posts
# -----------------------------------------------------------



@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),current_user=Depends(outh2.get_current_user)):
    """
    Retrieve all posts from the database.
    """
    # cursor.execute("SELECT * FROM posts;")
    # posts = cursor.fetchall()
    posts=db.query(models.Posts).all()
    return  posts


# -----------------------------------------------------------
# Create a new post
# -----------------------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db),current_user=Depends(outh2.get_current_user)):
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
    
    new_post=models.Posts(user_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# -----------------------------------------------------------
# Retrieve a single post by ID
# -----------------------------------------------------------
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db),current_user=Depends(outh2.get_current_user)):
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

    return  post


# -----------------------------------------------------------
# Delete a post by ID
# -----------------------------------------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user=Depends(outh2.get_current_user)):
    """
    Delete a post by ID.
    - Returns HTTP 404 if the post doesn't exist.
    - Returns 204 (No Content) upon success.
    """
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post=db.query(models.Posts).filter(models.Posts.id==id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )
    if post.first().user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    post.delete(synchronize_session=False)
    db.commit()     
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# -----------------------------------------------------------
# Update an existing post
# -----------------------------------------------------------
@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(outh2.get_current_user)
):
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
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    # ✅ Use .dict() instead of .model_dump()
    data = updated_post.dict(exclude_unset=True)
    data.pop("id", None)
    data.pop("created_at", None)

    post_query.update(data, synchronize_session=False)
    db.commit()

    return post_query.first()
