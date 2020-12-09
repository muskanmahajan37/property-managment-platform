from typing import Any

from sqlalchemy.orm import Session


def store_model(db: Session, model: Any) -> Any:
    """ Reusable function for storing specific models in the database"""
    db.add(model)
    db.commit()
    db.refresh(model)
    return model
