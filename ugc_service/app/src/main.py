from logging import DEBUG

import uvicorn
from aiohttp import ClientSession
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from logger import LOGGING_FORMAT
from src.api.v1 import film_views, auth, user_actions
from src.db import auth_utils as auth_session
from src.db.kafka_utils import kafka_container
from src.settings import settings

app = FastAPI(
    title=settings.project_name,
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://oauth.vk.com/access_token", "https://oauth.vk.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await kafka_container.start()
    auth_session.session = ClientSession(settings.auth_addr)


@app.on_event("shutdown")
async def shutdown():
    await kafka_container.stop()
    await auth_session.session.close()


app.include_router(auth.router, prefix='/api/v1/auth')
app.include_router(film_views.router, prefix="/api/v1/send_view_progress")
app.include_router(user_actions.router, prefix="/api/v1/user_actions")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        log_config=LOGGING_FORMAT,
        log_level=DEBUG,
    )
