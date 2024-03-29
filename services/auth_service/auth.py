from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service.auth_model import Token
from database.models import User
from database.hashing import Hash
from services.auth_service.token import create_access_token


def log_in(request: OAuth2PasswordRequestForm, db: Session):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Email address")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = create_access_token(data={"sub": user.email})
    user_id = get_user_id(request.username, db)
    token = Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user_id
    )
    return token


def log_in_while_creation(username: str, password: str, db: Session):
    user = db.query(User).filter(User.email == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Email address")

    if not Hash.verify(user.password, password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = create_access_token(data={"sub": user.email})
    token = Token(
        access_token=access_token,
        token_type="bearer"
    )
    return token


def get_user_id(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email {email} not found")
    return user.id
