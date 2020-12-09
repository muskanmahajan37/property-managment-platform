from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.flex.auth.dependencies import get_current_active_user, get_current_superuser
from src.flex.core.i18n import Messages
from src.flex.db.dependency import get_db
from src.flex.property import service as property_service
from src.flex.property.dependencies import (
    check_is_admin_or_property_owner,
    get_property_by_id_from_path,
)
from src.flex.property.models import Property
from src.flex.property.schemas import (
    PropertyCreate,
    PropertyRead,
    PropertyReadDetailed,
    PropertyUpdate,
)
from src.flex.user import service as user_service
from src.flex.user.models import User

api_router = APIRouter()


@api_router.post("", response_model=PropertyRead)
def create_property(
    user: User = Depends(get_current_active_user),
    *,
    property_create: PropertyCreate,
    db_session: Session = Depends(get_db),
) -> Any:
    service_in_db = property_service.create_property(
        db_session=db_session, property_in=property_create, user=user
    )
    return service_in_db


@api_router.get("/all", response_model=List[PropertyReadDetailed])
def get_all_properties(
    user: User = Depends(get_current_superuser), db_session: Session = Depends(get_db)
) -> Any:
    properties = property_service.get_all_properties(db_session=db_session)
    if not properties:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=Messages.ERR_NO_PROPERTY_FOUND
        )
    return properties


@api_router.get("/", response_model=List[PropertyRead])
def get_my_properties(
    user: User = Depends(get_current_active_user), db_session: Session = Depends(get_db)
) -> Any:
    properties = property_service.get_my_properties(db_session=db_session, user=user)
    if not properties:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=Messages.ERR_NO_PROPERTY_FOUND
        )
    return properties


@api_router.get(
    "/{property_id}",
    response_model=PropertyReadDetailed,
    dependencies=[Depends(check_is_admin_or_property_owner)],
)
def get_property_by_id(
    property_by_id: Property = Depends(get_property_by_id_from_path),
) -> Any:
    return property_by_id


@api_router.put(
    "/{property_id}",
    response_model=PropertyReadDetailed,
    dependencies=[Depends(check_is_admin_or_property_owner)],
)
def update_property(
    *,
    property_by_id: Property = Depends(get_property_by_id_from_path),
    property_update: PropertyUpdate,
    user: User = Depends(get_current_active_user),
    db_session: Session = Depends(get_db),
) -> Any:
    if property_update.user_id and not user.is_admin:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail=Messages.ERR_UNAUTHORIZED_TO_CHANGE_PROPERTY
        )
    if property_update.user_id and not user_service.get_by_id(property_update.user_id, db_session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=Messages.ERR_OWNER_OF_PROPERTY_NONE
        )
    return property_service.update_property(db_session, property_by_id, property_update)


@api_router.delete(
    "/{property_id}",
    response_model=PropertyRead,
    dependencies=[Depends(check_is_admin_or_property_owner)],
)
def delete_property(
    *,
    property_by_id: Property = Depends(get_property_by_id_from_path),
    db_session: Session = Depends(get_db),
) -> Any:
    return property_service.delete_property(db_session, property_by_id)
