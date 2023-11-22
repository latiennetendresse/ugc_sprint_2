import motor.motor_asyncio
from src.settings import settings


class MongoDBConnector:
    def __init__(self):
        self.client = None
        self.db = None

    async def start(self):
        if not self.client:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_host)
            self.db = self.client[settings.mongodb_database]

    async def stop(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None

    @property
    def database(self):
        return self.db


mongodb_connector = MongoDBConnector()


async def get_mongodb_database():
    await mongodb_connector.start()
    return mongodb_connector.database


async def close_mongodb_connection():
    await mongodb_connector.stop()
