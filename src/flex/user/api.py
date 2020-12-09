from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.flex.auth.dependencies import get_current_active_user, get_current_superuser
from src.flex.core.exceptions import EntityNotFoundException, NotAuthorizedException
from src.flex.core.i18n import Messages
from src.flex.db.dependency import get_db
from src.flex.user import service as user_service
from src.flex.user.models import User
from src.flex.user.schemas import UserCreateAdmin, UserRead, UserReadAdmin, UserUpdate

api_router = APIRouter()


@api_router.get("", response_model=List[UserReadAdmin])
def get_users(user: User = Depends(get_current_superuser), db: Session = Depends(get_db)) -> Any:
    users = user_service.get_all_users(db)
    if not users:
        raise HTTPException(status_code=404, detail=Messages.ERR_NO_USER_FOUND)
    return users


@api_router.post("", response_model=UserRead)
def create_user(
    user_create: UserCreateAdmin,
    user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
) -> Any:
    """Create a new user with admin role"""
    if user_service.get_by_username(user_create.username, db) or user_service.get_by_email(
        user_create.email, db
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=Messages.ERR_EMAIL_OR_USERNAME_ALREADY_EXISTS
        )
    return user_service.create_user_admin(user_create, db)


@api_router.delete("/{user_id}", response_model=UserRead)
def delete_user(
    user_id: int,
    user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
) -> Any:
    """Delete user, with admin role"""
    try:
        user = user_service.delete_user(user_id, db)  # type:  ignore
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return user


@api_router.put("/{user_id}", response_model=UserRead)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """Update user (Admin role)"""
    user = user_service.get_by_id(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Messages.ERR_USER_NOT_FOUND,
        )
    user = user_service.update_user(db, user_model=current_user, user_in=user_in)
    return user


@api_router.put("", response_model=UserRead)
def update_me(
    *,
    db: Session = Depends(get_db),
    password: str = Body(None),
    first_name: str = Body(None),
    last_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Update current logged in user"""
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if first_name is not None:
        user_in.first_name = first_name
    if last_name is not None:
        user_in.last_name = last_name
    if email is not None:
        user_in.email = email
    user = user_service.update_user(db, current_user, user_in)
    return user


@api_router.get("/me", response_model=UserRead)
def read_current_user(user: User = Depends(get_current_active_user)) -> Any:
    """Return data of the current logged in user"""
    return user
