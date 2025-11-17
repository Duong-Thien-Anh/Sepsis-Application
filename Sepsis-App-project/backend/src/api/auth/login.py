from dataclasses import dataclass
import http
import logging
import bcrypt
from fastapi import HTTPException
from pydantic import BaseModel

from ...state import login_limiter
from ...repositories import account
from ...utils.jwt import (
    TokenPair,
    create_token_pair,
)
from ..response import Response
from . import router


# ---- Exceptions ----
@dataclass
class InvalidCredentials(Exception):
    """
    # Cases:
    * Wrong password.
    * User not found.
    """

    msg: str


@dataclass
class ReachedLoginLimit(HTTPException):
    msg: str = "Bạn đã đăng nhập sai nhiều lần, vui lòng thử lại sau 5 phút."

    def __post_init__(self):
        super().__init__(
            status_code=400, detail=self.msg
        )


# ---------------------


class LoginDTO(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(
    dto: LoginDTO,
) -> Response[TokenPair]:
    await loginInternal(
        dto.username, dto.password
    )
    return Response(
        http.HTTPStatus.OK,
        create_token_pair(dto.username),
        "Đăng nhập thành công!",
    )


async def loginInternal(
    username: str, pwd: str
) -> None:
    result = await account.getFields(
        username,
        (account.Account.password_hash),
        False,
    )

    if result is None:
        raise InvalidCredentials(
            "Không tìm thấy người dùng!"
        )

    try:
        if login_limiter.isLimited(username):
            raise ReachedLoginLimit()

        hashed = result[0]
        is_verified = bcrypt.checkpw(
            pwd.encode("utf-8"),
            hashed.encode("utf-8"),
        )

        if not is_verified:
            raise InvalidCredentials(
                "Mật khẩu không đúng!"
            )
    except Exception as e:
        login_limiter.increase(username)
        raise e
