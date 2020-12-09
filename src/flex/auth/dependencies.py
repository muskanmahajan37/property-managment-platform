from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm.session import Session
from starlette import status

from src.flex.auth.schemas import TokenPayload
from src.flex.core.config import get_settings, settings
from src.flex.core.enums import Role
from src.flex.core.security import ALGORITHM
from src.flex.db.dependency import get_db
from src.flex.user import service as user_service
from src.flex.user.models import User

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{get_settings().API_PREFIX}/login/access-token")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = user_service.get_by_id(token_data.sub, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> Optional[User]:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")
    return current_user


def get_current_superuser(
    current_user: User = Depends(get_current_user),
) -> Optional[User]:
    if current_user.role != Role.ADMIN:
        raise HTTPException(400, detail="User has no previleges")
    return current_user
