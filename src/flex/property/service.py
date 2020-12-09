from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.flex.core.commons import store_model
from src.flex.property.models import Property, PropertyAddress
from src.flex.property.schemas import PropertyCreate, PropertyUpdate
from src.flex.user.models import User


def create_property(
    *, db_session: Session, property_in: PropertyCreate, user: User
) -> Optional[Property]:
    property = Property(**property_in.dict(exclude={"address"}), user=user)
    property.address = PropertyAddress(**property_in.address.dict())
    return store_model(db_session, property)


def get_all_properties(*, db_session: Session) -> Optional[List[Property]]:
    return db_session.query(Property).all()


def get_my_properties(*, db_session: Session, user: User) -> Optional[List[Property]]:
    properties = db_session.query(Property).filter(Property.user_id == user.id).all()
    if not properties:
        return None
    return properties


def get_property_by_id(*, db_session: Session, property_id: int) -> Optional[Property]:
    return db_session.query(Property).filter(Property.id == property_id).first()


def delete_property(db: Session, property_model: Property) -> Optional[Property]:
    db.delete(property_model.address)
    db.delete(property_model)
    db.commit()
    return property_model


def get_property_address(*, db_session: Session, property_address_id: int) -> PropertyAddress:
    return (
        db_session.query(PropertyAddress).filter(PropertyAddress.id == property_address_id).first()
    )


def update_property_address(
    db_session: Session, property_address: PropertyAddress, property_update: PropertyUpdate
) -> None:
    property_address_data = jsonable_encoder(property_address)
    update_data = property_update.address.dict(skip_defaults=True)  # type: ignore
    for field in property_address_data:
        if field in update_data:
            setattr(property_address, field, update_data[field])
    db_session.add(property_address)
    db_session.commit()


def update_property(
    db: Session, property_model: Property, property_update: PropertyUpdate
) -> Optional[Property]:
    property_data = jsonable_encoder(property_model)
    update_data = property_update.dict(skip_defaults=True, exclude={"address"})
    for field in property_data:
        if field in update_data:
            setattr(property_model, field, update_data[field])
    if property_update.address:
        update_property_address(
            db_session=db, property_address=property_model.address, property_update=property_update
        )
    db.add(property_model)
    db.commit()
    return property_model
