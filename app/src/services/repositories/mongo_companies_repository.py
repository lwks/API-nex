from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorClient

from app.src.helpers.object_id import ensure_object_id
from app.src.helpers.utils import coerce_dates_for_pymongo


class MongoCompaniesRepository:
    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        self._db = client[db_name]
        self._col = self._db["companies"]

    def _resolve_object_id(self, value: str) -> Any:
        return ensure_object_id(
            value,
            error_message="Invalid company identifier received.",
            dependency_message=(
                "ObjectId support is required to query companies using legacy identifiers."
            ),
        )

    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        # companies use the provided string id when available, but we also
        # support ObjectId lookup to keep behaviour consistent with other
        # collections.
        doc = await self._col.find_one({"_id": id})
        if doc:
            return doc
        object_id = self._resolve_object_id(id)
        return await self._col.find_one({"_id": object_id})

    async def create(self, data: Dict[str, Any]) -> str:
        payload = coerce_dates_for_pymongo(data)
        company_id = payload.pop("id", None)
        if company_id is not None:
            payload["_id"] = company_id
        res = await self._col.insert_one(payload)
        return str(res.inserted_id)

    async def update(self, id: str, data: Dict[str, Any]) -> bool:
        payload = coerce_dates_for_pymongo(data)
        res = await self._col.update_one({"_id": id}, {"$set": payload})
        if res.matched_count:
            return res.modified_count > 0 or bool(payload)
        object_id = self._resolve_object_id(id)
        res = await self._col.update_one({"_id": object_id}, {"$set": payload})
        return res.modified_count > 0 or res.matched_count > 0

    async def delete(self, id: str) -> bool:
        res = await self._col.delete_one({"_id": id})
        if res.deleted_count:
            return True
        object_id = self._resolve_object_id(id)
        res = await self._col.delete_one({"_id": object_id})
        return res.deleted_count > 0

    async def list(self, *, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        cursor = self._col.find().skip(skip).limit(limit)
        return [doc async for doc in cursor]
