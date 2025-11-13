from datetime import date, datetime
import http
from typing import Annotated
from fastapi import Security
from pydantic import BaseModel

from ...utils import jwt
from ..response import Response
from src.repositories import (
    account as account_repository,
)
from . import router


class AccountResponse(BaseModel):
    account_id: int
    username: str
    password_hash: str
    full_name: str
    email: str
    phone: str
    role: str
    status: str
    created_date: date
    last_login: datetime
    note: str | None
    is_2fa_enabled: bool
    last_login_ip: str
    login_method: str

    class Config:
        from_attributes = True


@router.get("")
async def getAll(
    _: Annotated[
        None,
        Security(jwt.checkRole, scopes=["admin"]),
    ],
) -> Response[list[AccountResponse]]:
    # TODO: just admin can use this feature
    return Response(
        http.HTTPStatus.OK,
        await getAllInternal(),
        "Lấy danh sách tài khoản thành công!",
    )


async def getAllInternal() -> list[
    AccountResponse
]:
    accounts = await account_repository.getAll()
    return [
        AccountResponse.model_validate(acc)
        for acc in accounts
    ]
