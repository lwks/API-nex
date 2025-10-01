from datetime import date, datetime
from typing import Any, Dict


def coerce_dates_for_pymongo(data: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy with date values converted to naive datetimes for PyMongo."""
    coerced: Dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, date) and not isinstance(value, datetime):
            coerced[key] = datetime.combine(value, datetime.min.time())
        else:
            coerced[key] = value
    return coerced
