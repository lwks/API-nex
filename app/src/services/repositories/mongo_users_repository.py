from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId


class MongoUsersRepository:
    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        self._db = client[db_name]
        self._col = self._db["users"]

    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        try:
            _id = ObjectId(id)
        except Exception:
            return None
        return await self._col.find_one({"_id": _id})

    async def create(self, data: Dict[str, Any]) -> str:
        res = await self._col.insert_one(data)
        return str(res.inserted_id)
