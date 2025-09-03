from dataclasses import dataclass

@dataclass
class Pagination:
    skip: int = 0
    limit: int = 20

    @staticmethod
    def clamp(skip: int | None, limit: int | None, *, max_limit: int = 100) -> "Pagination":
        _skip = max(0, skip or 0)
        _limit = min(max_limit, max(1, limit or 20))
        return Pagination(skip=_skip, limit=_limit)
