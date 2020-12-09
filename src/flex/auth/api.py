from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.flex.core import security
from src.flex.core.config import settings
from src.flex.core.exceptions import EntityNotFoundException, PasswordNotCorrectException
from src.flex.db.dependency import get_db
from src.flex.user import schemas
from src.flex.user import service as user_service
from src.flex.user.schemas import UserRead

api_router = APIRouter()


@api_router.post("/login/access-token")
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Any:
    try:
        user = user_service.authenticate(
            email=form_data.username, password=form_data.password, db=db
        )
    except EntityNotFoundException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except PasswordNotCorrectException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=(str(e)))
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "user": UserRead.from_orm(user),
        "access_token": security.create_access_token(
            subject=user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@api_router.post("/register", response_model=schemas.UserRead)
def sign_up(user_create: schemas.UserCreate, db: Session = Depends(get_db)) -> Any:
    user = user_service.get_by_email(user_create.email, db=db)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return user_service.create(user_create, db)
