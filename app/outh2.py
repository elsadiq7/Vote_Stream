"""
OAuth2 authentication and token management.
"""
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, database, models
from .config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict) -> str:
    """
    Creates a new access token.

    Args:
        data (dict): The data to encode in the token.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    # Set expiration time for the token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Encode the data using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception: HTTPException) -> schemas.TokenData:
    """
    Verifies the access token.

    Args:
        token (str): The JWT token to verify.
        credentials_exception (HTTPException): Exception to raise if verification fails.

    Returns:
        schemas.TokenData: The token data extracted from the token.

    Raises:
        credentials_exception: If the token is invalid or the user ID is missing.
    """
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)) -> models.Users:
    """
    Dependency to get the current authenticated user.

    Args:
        token (str): The JWT token.
        db (Session): The database session.

    Returns:
        models.Users: The authenticated user object.

    Raises:
        HTTPException: If credentials are invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify the token and get the user ID
    token_data = verify_access_token(token, credentials_exception)
    
    # Query the database for the user
    user = db.query(models.Users).filter(models.Users.id == token_data.id).first()
    return user