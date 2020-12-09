"""Provide a mixin that tracks creation and update timestamps."""
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr


def timezone_aware_now() -> datetime:
    """Return the date and time in this moment in the universal timezone."""
    return datetime.now(timezone.utc)


class TimestampMixin:
    """
    Define creation and update time columns to be mixed in with other tables.
    Attributes
    ----------
    created_at : datetime
        By default this value is populated at instantiation with the time of
        the moment.
    updated_at : datetime
        The time is automatically populated whenever the database model is
        updated.
    """

    @declared_attr
    def created_at(self) -> Any:
        return Column(DateTime(timezone=True), nullable=False, default=timezone_aware_now)

    @declared_attr
    def updated_at(self) -> Any:
        return Column(DateTime(timezone=True), nullable=True, onupdate=timezone_aware_now)


class CustomMixin(object):
    id = Column(Integer, primary_key=True, index=True)
