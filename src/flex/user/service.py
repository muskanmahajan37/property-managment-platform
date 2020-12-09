from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.flex.core import security
from src.flex.core.commons import store_model
from src.flex.core.enums import Role
from src.flex.core.exceptions import (
    EntityNotFoundException,
    NotAuthorizedException,
    PasswordNotCorrectException,
)
from src.flex.user.models import User
from src.flex.user.schemas import UserCreate, UserCreateAdmin, UserUpdate


def get_by_id(id: int, db: Session) -> Optional[User]:
    return db.query(User).filter(User.id == id).one_or_none()


def is_active(user: User) -> bool:
    return user.is_active


def get_by_email(email: str, db: Session) -> Optional[User]:
    return db.query(User).filter(User.email == email).one_or_none()


def get_all_users(db: Session) -> Optional[List[User]]:
    return db.query(User).all()


def get_role(user: User) -> str:
    return str(user.role)


def get_by_username(username: str, db: Session) -> Optional[User]:
    return db.query(User).filter(User.username == username).one_or_none()


def create(user_create: UserCreate, db: Session) -> User:
    user = User(
        email=user_create.email,
        username=user_create.username,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        hashed_password=security.get_password_hash(user_create.password),
    )
    store_model(db, user)
    return user


def create_user_admin(user_create: UserCreateAdmin, db: Session) -> User:
    user = User(
        **user_create.dict(exclude={"password"}),
        hashed_password=security.get_password_hash(user_create.password),
    )
    store_model(db, user)
    return user


def authenticate(email: str, password: str, db: Session) -> User:
    user = get_by_email(email, db)
    if not user:
        raise EntityNotFoundException("User not found")
    if not security.verify_password(password, user.hashed_password):
        raise PasswordNotCorrectException("Password not correct")
    return user


def delete_user(user_id: int, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise EntityNotFoundException(f"User with id:[{user_id}] not found!")
    if user.role == Role.ADMIN:
        raise NotAuthorizedException("You cannot delete another admin")
    db.delete(user)
    db.commit()
    return user


def update_user(db_session: Session, user_model: User, user_in: UserUpdate) -> Optional[User]:
    user_data = jsonable_encoder(user_model)
    update_data = user_in.dict(skip_defaults=True)
    if "password" in update_data:
        hashed_password = security.get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    for field in user_data:
        if field in update_data:
            setattr(user_model, field, update_data[field])
    db_session.add(user_model)
    db_session.commit()
    db_session.refresh(user_model)
    return store_model(db_session, user_model)
