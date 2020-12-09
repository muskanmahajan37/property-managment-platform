from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.flex.user import user_service
from src.flex.user.schemas import UserCreate


def test_create_user(db: Session) -> None:
    email = EmailStr("valon@gmail.com")
    password = "password"
    first_name = "Valon"
    last_name = "diqka"
    user_in = UserCreate(first_name=first_name, last_name=last_name, email=email, password=password)
    user = user_service.create(user_create=user_in, db=db)
    assert user.email == email
    assert user.last_name == last_name
