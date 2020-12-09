from enum import Enum


class Role(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class PropertyType(str, Enum):
    industrial = "INDUSTRIAL"
    land = "LAND"
    office = "OFFICE"
    multi_family = "MULTI_FAMILY"
    other = "OTHER"


class PropertyStatus(str, Enum):
    active = "ACTIVE"
    inactive = "INACTIVE"
