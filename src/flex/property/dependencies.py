from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.flex.auth.dependencies import get_current_active_user
from src.flex.core.i18n import Messages
from src.flex.db.dependency import get_db
from src.flex.property import service as property_service
from src.flex.property.models import Property
from src.flex.user.models import User


def get_property_by_id_from_path(
    *,
    property_id: int,
    db_session: Session = Depends(get_db),
) -> Property:
    property_by_id = property_service.get_property_by_id(
        db_session=db_session, property_id=property_id
    )
    if not property_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Messages.ERR_PROPERTY_NOT_FOUND.format(id=property_id),
        )
    return property_by_id


def check_is_admin_or_property_owner(
    *,
    property_by_id: Property = Depends(get_property_by_id_from_path),
    user: User = Depends(get_current_active_user),
) -> None:
    if property_by_id.user_id != user.id and not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=Messages.ERR_NOT_AUTHORIZED)
