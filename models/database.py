"""
Database layer for HiddenYatra — Backward Compatibility Shim.
Re-exports core database modules. Domain modules will be added
as they are implemented in subsequent development milestones.
"""

from models.connection import (
    get_db, get_cursor, init_db, slugify, _slugify, _escape_like
)
from models.constants import (
    PLACE_CATEGORIES, SPECIALTY_CATEGORIES, ACCOMMODATION_TYPES,
    SERVICE_GROUP_ORDER, get_category_label
)
