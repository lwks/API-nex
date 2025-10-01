from typing import Any

from app.src.helpers.custom_exception import InvalidIdentifierError, custom_exception

_DEFAULT_DEPENDENCY_MESSAGE = (
    "ObjectId support is not available. Install pymongo (or bson) to enable this feature."
)


def ensure_object_id(
    value: str,
    *,
    error_message: str,
    dependency_message: str | None = None,
) -> Any:
    """Return a Mongo-compatible ObjectId instance or raise a custom error."""
    try:
        from bson import ObjectId  # type: ignore
    except ModuleNotFoundError as exc:
        raise custom_exception(
            InvalidIdentifierError,
            dependency_message or _DEFAULT_DEPENDENCY_MESSAGE,
            original_exception=exc,
        ) from exc

    try:
        return ObjectId(value)
    except BaseException as exc:  # pragma: no cover - bson handles validation internally
        raise custom_exception(
            InvalidIdentifierError,
            error_message,
            original_exception=exc,
        ) from exc
