"""
API Router for managing posts.
"""
from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, outh2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(outh2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    """
    Retrieve all posts with pagination and search.

    Args:
        db (Session): Database session.
        current_user (models.Users): Authenticated user.
        limit (int): Number of posts to return.
        skip (int): Number of posts to skip.
        search (Optional[str]): Search query for post titles.

    Returns:
        List[schemas.PostOut]: A list of posts with vote counts.
    """
    # Perform a left outer join to get vote counts for each post
    # group_by is essential when using aggregate functions like count
    results = (
        db.query(models.Posts,
                 func.count(models.Votes.post_id).label("vote"))
          .join(models.Votes, models.Votes.post_id == models.Posts.id, isouter=True)
          .filter(models.Posts.title.ilike(f"%{search}%"))
          .group_by(models.Posts.id)
          .limit(limit)
          .offset(skip)
          .all()
    )

    # Convert the query results (list of tuples) into a list of dictionaries
    # This matches the expected response model structure
    output = []
    for post, vote in results:
        output.append({
            "Post": post,
            "vote": vote
        })

    return output


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(outh2.get_current_user)
):
    """
    Create a new post.

    Args:
        post (schemas.PostCreate): Post data.
        db (Session): Database session.
        current_user (models.Users): Authenticated user.

    Returns:
        models.Posts: The created post.
    """
    new_post = models.Posts(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(outh2.get_current_user)
):
    """
    Retrieve a single post by ID.

    Args:
        id (int): Post ID.
        db (Session): Database session.
        current_user (models.Users): Authenticated user.

    Returns:
        schemas.PostOut: The post with vote count.

    Raises:
        HTTPException: If the post is not found.
    """
    post = (
        db.query(models.Posts,
                 func.count(models.Votes.post_id).label("vote"))
          .join(models.Votes, models.Votes.post_id == models.Posts.id, isouter=True)
          .filter(models.Posts.id == id)
          .group_by(models.Posts.id)
          .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )

    post_obj, vote_count = post

    return {
        "Post": post_obj,
        "vote": vote_count
    }


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(outh2.get_current_user)
):
    """
    Delete a post by ID.

    Args:
        id (int): Post ID.
        db (Session): Database session.
        current_user (models.Users): Authenticated user.

    Raises:
        HTTPException: If the post is not found or user is not authorized.
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
    
    post_query.delete(synchronize_session=False)
    db.commit()     
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(outh2.get_current_user)
):
    """
    Update a post by its ID.

    Args:
        id (int): Post ID.
        updated_post (schemas.PostCreate): Updated post data.
        db (Session): Database session.
        current_user (models.Users): Authenticated user.

    Returns:
        models.Posts: The updated post.

    Raises:
        HTTPException: If the post is not found or user is not authorized.
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

    data = updated_post.dict(exclude_unset=True)
    data.pop("id", None)
    data.pop("created_at", None)

    post_query.update(data, synchronize_session=False)
    db.commit()

    return post_query.first()
