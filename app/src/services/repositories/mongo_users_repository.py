from typing import Optional, Dict, Any

from motor.motor_asyncio import AsyncIOMotorClient

from app.src.helpers.object_id import ensure_object_id


class MongoUsersRepository:
    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        self._db = client[db_name]
        self._col = self._db["users"]

    def _resolve_object_id(self, value: str) -> Any:
        return ensure_object_id(
            value,
            error_message="Invalid user identifier received.",
            dependency_message=(
                "ObjectId support is required to query users using legacy identifiers."
            ),
        )

    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        _id = self._resolve_object_id(id)
        return await self._col.find_one({"_id": _id})

    async def create(self, data: Dict[str, Any]) -> str:
        res = await self._col.insert_one(data)
        return str(res.inserted_id)
