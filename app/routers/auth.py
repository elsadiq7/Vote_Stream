"""
API Router for authentication.
"""
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas
from .. import models, utils, database, outh2

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    """
    Authenticate a user and return an access token.

    Args:
        user_credentials (OAuth2PasswordRequestForm): Login credentials (username/email and password).
        db (Session): Database session.

    Returns:
        dict: Access token and token type.

    Raises:
        HTTPException: If credentials are invalid.
    """
    # Find the user by email
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Verify the password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Create an access token
    token = outh2.create_access_token(data={"user_id": user.id})
    
    return {"access_token": token, "token_type": "bearer"}
