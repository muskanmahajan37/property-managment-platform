import re

from sqlalchemy.ext.declarative import declarative_base, declared_attr

from .mixins import CustomMixin, TimestampMixin


class CustomBase(TimestampMixin, CustomMixin):
    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()


Base = declarative_base(cls=CustomBase)
