from functools import lru_cache

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from src.db.mongo_utils import get_mongodb_database


class UserActionService:
    def __init__(self, mongo: AsyncIOMotorClient) -> None:
        self.mongo = mongo

    async def send_like(self, user_id: str, film_id: int) -> None:
        await self.mongo.db.likes.insert_one(
            {'user_id': user_id, 'film_id': film_id}
        )

    async def add_to_bookmarks(self, user_id: str, film_id: int) -> None:
        await self.mongo.db.bookmarks.insert_one(
            {'user_id': user_id, 'film_id': film_id}
        )

    async def add_review(self, user_id: str, film_id: int) -> None:
        await self.mongo.db.reviews.insert_one(
            {'user_id': user_id, 'film_id': film_id}
        )


@lru_cache()
def get_user_action_service(
    mongo: AsyncIOMotorClient = Depends(get_mongodb_database),
) -> UserActionService:
    return UserActionService(mongo)
