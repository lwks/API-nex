from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, Iterable, Mapping


def _convert_value(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        # DynamoDB does not support date/datetime types directly
        return value.isoformat()
    if isinstance(value, float):
        # Use Decimal to preserve precision across DynamoDB operations
        return Decimal(str(value))
    if isinstance(value, Mapping):
        return {k: _convert_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_convert_value(v) for v in value]
    if isinstance(value, tuple):
        return [_convert_value(v) for v in value]
    return value


def serialize_for_dynamodb(payload: Mapping[str, Any] | Iterable[tuple[str, Any]]) -> Dict[str, Any]:
    """
    Convert a dictionary-like payload into a DynamoDB-compatible structure.
    """
    if isinstance(payload, Mapping):
        items = payload.items()
    else:
        items = payload
    return {key: _convert_value(value) for key, value in items}


def deserialize_from_dynamodb(item: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Convert a DynamoDB item into plain Python primitives.
    """
    def _restore(value: Any) -> Any:
        if isinstance(value, Decimal):
            # Use int when possible, otherwise float for backwards compatibility
            return int(value) if value == int(value) else float(value)
        if isinstance(value, Mapping):
            return {k: _restore(v) for k, v in value.items()}
        if isinstance(value, list):
            return [_restore(v) for v in value]
        return value

    return {key: _restore(value) for key, value in item.items()}
