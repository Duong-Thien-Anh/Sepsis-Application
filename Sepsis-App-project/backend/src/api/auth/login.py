from dataclasses import dataclass
import http
import bcrypt
from pydantic import BaseModel
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

    hashed = result[0]
    is_verified = bcrypt.checkpw(
        pwd.encode("utf-8"),
        hashed.encode("utf-8"),
    )

    if not is_verified:
        raise InvalidCredentials(
            "Mật khẩu không đúng!"
        )

    return
