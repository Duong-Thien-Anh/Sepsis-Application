from dataclasses import dataclass
from datetime import datetime
import http
import bcrypt
from fastapi import HTTPException, Request
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
def login(
    dto: LoginDTO,
    request: Request,
) -> Response[TokenPair]:
    host = request.client.host
    loginInternal(
        dto.username, dto.password, host
    )
    return Response(
        http.HTTPStatus.OK,
        create_token_pair(dto.username),
        "Đăng nhập thành công!",
    )


def loginInternal(
    username: str, pwd: str, host: str
) -> None:
    result = account.getFields(
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

        # Update information each login time
        account.updateFields(
            username,
            (
                account.Account.last_login,
                account.Account.last_login_ip,
            ),
            (datetime.today(), host),
        )
    except Exception as e:
        login_limiter.increase(username)
        raise e
