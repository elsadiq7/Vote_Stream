"""
API Router for voting on posts.
"""
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, outh2, database

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: models.Users = Depends(outh2.get_current_user)
):
    """
    Vote on a post (upvote or remove vote).

    Args:
        vote (schemas.Vote): Vote data (post_id and direction).
        db (Session): Database session.
        current_user (models.Users): Authenticated user.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If vote conflict (already voted) or vote not found (when removing).
    """
    # Check if the post exists
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
"""
API Router for voting on posts.
"""
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, outh2, database

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: models.Users = Depends(outh2.get_current_user)
):
    """
    Vote on a post (upvote or remove vote).

    Args:
        vote (schemas.Vote): Vote data (post_id and direction).
        db (Session): Database session.
        current_user (models.Users): Authenticated user.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If vote conflict (already voted) or vote not found (when removing).
    """
    # Check if the post exists
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist"
        )

    # Check if the user has already voted on this post
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id,
        models.Votes.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        # Logic for adding a vote (upvote)
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}",
            )
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        # Logic for removing a vote (downvote/unvote)
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist",
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}