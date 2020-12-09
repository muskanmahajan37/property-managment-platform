from typing import Optional

from pydantic import Field

from src.flex.core.api_model import APIModel
from src.flex.core.enums import PropertyStatus, PropertyType


class PropertyBase(APIModel):
    name: Optional[str]
    type: Optional[PropertyType]
    status: Optional[PropertyStatus]
    size: Optional[int]


class PropertyAddressBase(APIModel):
    country: Optional[str]
    city: Optional[str]
    address: Optional[str]
    zip_code: Optional[str]


class PropertyOwnerRead(APIModel):
    id: int = Field(alias="user_id")
    first_name: str
    last_name: str


class PropertyRead(PropertyBase):
    id: int
    address: PropertyAddressBase


class PropertyAddressCreate(PropertyAddressBase):
    country: str
    city: str
    address: str
    zip_code: str


class PropertyCreate(PropertyBase):
    name: str
    type: PropertyType
    status: PropertyStatus
    size: int
    address: PropertyAddressCreate


class PropertyUpdate(PropertyBase):
    user_id: Optional[int]
    address: Optional[PropertyAddressBase]


class PropertyReadDetailed(PropertyBase):
    id: Optional[int]
    address: Optional[PropertyAddressBase]
    user: PropertyOwnerRead = Field(None, alias="owner")
