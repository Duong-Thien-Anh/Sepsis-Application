from dataclasses import dataclass
import http
from os import environ
import re
import bcrypt
from fastapi import Security
from pydantic import (
    BaseModel,
    field_validator,
)


from ...repositories import (
    account as account_repository,
)

from ...utils import jwt
from ..response import Response


from . import router

VIETNAM_PHONE_REGEX = re.compile(
    r"^0[1-9][0-9]{8,9}$"
)


# ---- Exceptions ----
@dataclass
class InvalidEmailFormat(Exception):
    msg: str


@dataclass
class InvalidPhoneFormat(Exception):
    pass


class UserExisted(Exception):
    pass


# ---------------------


class SignUpDTO(BaseModel):
    username: str
    password: str
    full_name: str
    email: str
    phone: str
    note: str

    @field_validator("email")
    @classmethod
    def validate_vn_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not v:
            raise InvalidEmailFormat(
                "Email không được để trống"
            )
        if "@" not in v:
            raise InvalidEmailFormat(
                "Email phải chứa ký tự @"
            )
        if not re.match(
            r"^[^@]+@[^@]+\.[^@]+$", v
        ):
            raise InvalidEmailFormat(
                "Email không hợp lệ. Ví dụ đúng: abc@gmail.com"
            )
        return v

    @field_validator("phone")
    @classmethod
    def validate_vn_phone(cls, v: str) -> str:
        v = re.sub(r"\D", "", v)

        if not VIETNAM_PHONE_REGEX.match(v):
            raise InvalidPhoneFormat
        return v


dependencies = []
if environ.get("ENV", "DEV") == "PRODUCTION":
    dependencies = [
        Security(jwt.checkRole, scopes=["admin"]),
    ]


@router.post(
    "/signup",
    dependencies=dependencies,
)
async def signup(
    dto: SignUpDTO,
) -> Response[None]:
    await signupInternal(dto)
    return Response(
        http.HTTPStatus.OK,
        None,
        "Đăng ký thành công!",
    )


async def signupInternal(dto: SignUpDTO) -> None:
    hashed = bcrypt.hashpw(
        dto.password.encode("utf-8"),
        bcrypt.gensalt(
            rounds=int(
                environ.get("APP_HASH_ROUND", 12)
            )
        ),
    )

    await account_repository.insertOne(
        dto.username,
        hashed.decode("utf-8"),
        dto.full_name,
        dto.email,
        dto.phone,
        dto.note,
    )
