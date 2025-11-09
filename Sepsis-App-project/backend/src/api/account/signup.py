import http
from os import environ
import re
import bcrypt
from pydantic import (
    BaseModel,
    Field,
    field_validator,
)

from ...error import (
    InvalidEmailFormat,
    InvalidPhoneFormat,
)

from ..response import Response
from ...repositories import (
    account as account_repository,
)

from . import router

VIETNAM_PHONE_REGEX = re.compile(
    r"^0[1-9][0-9]{8,9}$"
)


class SignUpDTO(BaseModel):
    username: str
    password: str
    full_name: str
    email: str
    phone: str
    role: str
    status: str
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


@router.post("")
async def signup(
    dto: SignUpDTO,
) -> Response[None]:
    # TODO: just admin can use this feature
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

    account_repository.insertOne(
        dto.username,
        hashed.decode("utf-8"),
        dto.full_name,
        dto.email,
        dto.phone,
        dto.note,
    )
