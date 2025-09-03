from typing import Sequence, Optional, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

class MongoItemsRepository:
    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        self._db = client[db_name]
        self._col = self._db["items"]

    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        try:
            _id = ObjectId(id)
        except Exception:
            return None
        return await self._col.find_one({"_id": _id})

    async def create(self, data: Dict[str, Any]) -> str:
        res = await self._col.insert_one(data)
        return str(res.inserted_id)

    async def update(self, id: str, data: Dict[str, Any]) -> bool:
        try:
            _id = ObjectId(id)
        except Exception:
            return False
        res = await self._col.update_one({"_id": _id}, {"$set": data})
        return res.modified_count > 0

    async def delete(self, id: str) -> bool:
        try:
            _id = ObjectId(id)
        except Exception:
            return False
        res = await self._col.delete_one({"_id": _id})
        return res.deleted_count > 0

    async def list(self, *, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        cursor = self._col.find().skip(skip).limit(limit)
        return [doc async for doc in cursor]
