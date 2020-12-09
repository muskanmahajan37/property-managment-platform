from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.flex.db.base_class import Base

if TYPE_CHECKING:
    from src.flex.user.models import User  # noqa: F401


class Property(Base):
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    size = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    address_id = Column(
        Integer,
        ForeignKey("property_address.id", ondelete="CASCADE"),
        nullable=False,
    )

    user = relationship("User", back_populates="properties")
    address = relationship("PropertyAddress", back_populates="property")


class PropertyAddress(Base):
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    address = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)

    property = relationship("Property", back_populates="address")
