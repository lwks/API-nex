from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.src.aws_services.dynamodb_service import DynamoDBService
from app.src.helpers.custom_exception import InvalidIdentifierError
from app.src.helpers.dynamodb import deserialize_from_dynamodb, serialize_for_dynamodb


class DynamoVagasRepository:
    """Repository implementation backed by DynamoDB for Job openings (Vagas)."""

    def __init__(self, service: DynamoDBService, *, partition_key: str = "id") -> None:
        self._service = service
        self._partition_key = partition_key

    def _build_key(self, identifier: str) -> Dict[str, Any]:
        if not identifier:
            raise InvalidIdentifierError("Vaga identifier cannot be empty.")
        return {self._partition_key: identifier}

    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        item = await self._service.get(self._build_key(id))
        if item is None:
            return None
        return deserialize_from_dynamodb(item)

    async def create(self, data: Dict[str, Any]) -> str:
        vaga_id = data.get("id") or str(uuid4())
        payload = {self._partition_key: vaga_id, **data}
        serialized = serialize_for_dynamodb(payload)
        await self._service.create(serialized)
        return vaga_id

    async def update(self, id: str, data: Dict[str, Any]) -> bool:
        if not data:
            return True
        key = self._build_key(id)
        serialized = serialize_for_dynamodb(data)
        updated = await self._service.update(key, serialized)
        return bool(updated)

    async def delete(self, id: str) -> bool:
        key = self._build_key(id)
        return await self._service.delete(key)

    async def list(self, *, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        fetch_limit = (skip + limit) if limit is not None else None
        items = await self._service.list(limit=fetch_limit)
        deserialized = [deserialize_from_dynamodb(item) for item in items]
        if skip:
            deserialized = deserialized[skip:]
        if limit is not None:
            deserialized = deserialized[:limit]
        return deserialized
