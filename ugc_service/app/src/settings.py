import os
from pydantic import Field

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = Field('ugc_service_app', env='PROJECT_NAME')
    kafka_host: str = Field('broker', env='KAFKA_HOST')
    kafka_port: int = Field(29092, env='KAFKA_PORT')
    auth_addr: str = Field('https://auth_service_nginx', env='AUTH_ADDR')
    mongodb_host: str = Field('localhost', env='MONGODB_HOST')
    mongodb_port: int = Field(27017, env='MONGODB_PORT')
    mongodb_database: str = Field('mydatabase', env='MONGODB_DATABASE')
    mongodb_collection: str = Field('objects', env='MONGODB_COLLECTION')


print(os.getenv("ENV_FILE"))

settings = Settings(_env_file=os.getenv("ENV_FILE"))
