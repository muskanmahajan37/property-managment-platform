from sqlalchemy import Boolean, Column, Enum, String
from sqlalchemy.orm import relationship

from src.flex.core.enums import Role
from src.flex.db.base_class import Base
from src.flex.property.models import Property  # noqa: F401


class User(Base):
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Role), nullable=False, default=Role.USER)

    properties = relationship("Property", back_populates="user", uselist=True)

    @property
    def is_admin(self) -> bool:
        return self.role == Role.ADMIN
