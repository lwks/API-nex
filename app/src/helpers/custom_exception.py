from typing import Type, TypeVar


T = TypeVar("T", bound="CustomBaseException")


class CustomBaseException(BaseException):
    def __init__(
        self,
        message: str,
        *,
        original_exception: BaseException | None = None,
    ) -> None:
        super().__init__(message)
        self.original_exception = original_exception


def custom_exception(
    exc_type: Type[T],
    message: str,
    *,
    original_exception: BaseException | None = None,
) -> T:
    return exc_type(message, original_exception=original_exception)


class InvalidIdentifierError(CustomBaseException):
    """Raised when a repository receives an invalid identifier."""
