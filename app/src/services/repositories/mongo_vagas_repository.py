from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorClient
from bson.errors import InvalidId
from bson.objectid import ObjectId

from app.src.helpers.utils import coerce_dates_for_pymongo


class MongoVagasRepository:
    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        self._db = client[db_name]
        self._col = self._db["vagas"]

    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        doc = await self._col.find_one({"_id": id})
        if doc:
            return doc
        try:
            object_id = ObjectId(id)
        except InvalidId:
            return None
        return await self._col.find_one({"_id": object_id})

    async def create(self, data: Dict[str, Any]) -> str:
        payload = coerce_dates_for_pymongo(data)
        res = await self._col.insert_one(payload)
        return str(res.inserted_id)

    async def update(self, id: str, data: Dict[str, Any]) -> bool:
        payload = coerce_dates_for_pymongo(data)
        res = await self._col.update_one({"_id": id}, {"$set": payload})
        if res.matched_count:
            return res.modified_count > 0 or bool(payload)
        try:
            object_id = ObjectId(id)
        except InvalidId:
            return False
        res = await self._col.update_one({"_id": object_id}, {"$set": payload})
        return res.modified_count > 0 or res.matched_count > 0

    async def delete(self, id: str) -> bool:
        res = await self._col.delete_one({"_id": id})
        if res.deleted_count:
            return True
        try:
            object_id = ObjectId(id)
        except InvalidId:
            return False
        res = await self._col.delete_one({"_id": object_id})
        return res.deleted_count > 0

    async def list(self, *, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        cursor = self._col.find().skip(skip).limit(limit)
        return [doc async for doc in cursor]
