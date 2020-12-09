#!/usr/bin/env python3
import logging

from src.flex.core.config import settings
from src.flex.core.enums import Role
from src.flex.db.session import SessionLocal
from src.flex.user.schemas import UserCreateAdmin
from src.flex.user.service import create_user_admin, get_by_email

logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    user = get_by_email(email=settings.FIRST_SUPERUSER_EMAIL, db=db)
    if not user:
        create_user_admin(
            UserCreateAdmin(
                first_name="Valon",
                last_name="Januzaj",
                username="vjanz",
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_active=True,
                role=Role.ADMIN,
            ),
            db,
        )


if __name__ == "__main__":
    init()
