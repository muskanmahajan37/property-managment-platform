from typing import Optional

from pydantic import EmailStr

from src.flex.core.api_model import APIModel
from src.flex.core.enums import Role


class UserBase(APIModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None


class UserCreate(UserBase):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str


class UserCreateAdmin(UserCreate):
    first_name: str
    last_name: str
    role: Role


class UserReadAdmin(UserBase):
    id: int
    role: Role


class UserRead(UserBase):
    pass


class UserUpdate(UserBase):
    password: Optional[str]
    role: Optional[Role]
