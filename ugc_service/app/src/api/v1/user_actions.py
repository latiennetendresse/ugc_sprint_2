from http import HTTPStatus

import jwt
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette.responses import Response

from src.models.data import TokenResponse
from src.services.user_actions import UserActionService, get_user_action_service


SECRET_KEY = "secretfghjrtyui"
ALGORITHM = "HS256"

router = APIRouter()

api_key_scheme = APIKeyHeader(name="Authorization")


async def get_decode_token(
    token: str = Depends(api_key_scheme),
) -> TokenResponse | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenResponse(**payload)
    except jwt.ExpiredSignatureError as ex:
        raise HTTPException(status_code=401, detail="Token has expired") from ex
    except jwt.PyJWTError as ex:
        raise HTTPException(status_code=401, detail="Invalid token") from ex


@router.post(
    "/like",
    status_code=HTTPStatus.OK,
    tags=["user_actions"],
    description="отправить лайк",
    summary="отправить лайк",
)
async def send_like(
    film_id: int,
    token: TokenResponse = Depends(get_decode_token),
    service: UserActionService = Depends(get_user_action_service),
) -> Response:
    await service.send_like(token.sub, film_id)
    return Response(status_code=HTTPStatus.OK)


@router.post(
    "/bookmark",
    status_code=HTTPStatus.OK,
    tags=["user_actions"],
    description="добавить в закладки",
    summary="добавить в закладки",
)
async def add_to_bookmarks(
    film_id: int,
    token: TokenResponse = Depends(get_decode_token),
    service: UserActionService = Depends(get_user_action_service),
) -> Response:
    await service.add_to_bookmarks(token.sub, film_id)
    return Response(status_code=HTTPStatus.OK)


@router.post(
    "/review",
    status_code=HTTPStatus.OK,
    tags=["user_actions"],
    description="добавить рецензию",
    summary="добавить рецензию",
)
async def add_review(
    film_id: int,
    token: TokenResponse = Depends(get_decode_token),
    service: UserActionService = Depends(get_user_action_service),
) -> Response:
    await service.add_review(token.sub, film_id)
    return Response(status_code=HTTPStatus.OK)
