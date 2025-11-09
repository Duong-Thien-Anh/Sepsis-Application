from datetime import date, datetime
import http
from pydantic import BaseModel
from ..response import Response
from src.repositories import (
    account as account_repository,
)

from . import router, log


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
def getAll() -> Response[list[AccountResponse]]:
    # TODO: just admin can use this feature
    return Response(
        http.HTTPStatus.OK,
        getAllInternal(),
        "Get all account successfully!",
    )


def getAllInternal() -> list[AccountResponse]:
    accounts = account_repository.getAll()

    log.info(accounts)

    return [
        AccountResponse.model_validate(acc)
        for acc in accounts
    ]
