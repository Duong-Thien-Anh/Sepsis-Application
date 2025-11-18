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

from .. import VIETNAM_PHONE_REGEX


from ...repositories import (
    base,
    account as account_repository,
    profile as profile_repository,
)

from ...utils import jwt, code
from ..response import Response


from . import router


# ---- Exceptions ----
@dataclass
class InvalidEmailFormat(Exception):
    msg: str


@dataclass
class InvalidPhoneFormat(Exception):
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
def signup(
    dto: SignUpDTO,
) -> Response[None]:
    signupInternal(dto)
    return Response(
        http.HTTPStatus.OK,
        None,
        "Đăng ký thành công!",
    )


def signupInternal(dto: SignUpDTO) -> None:
    hashed = bcrypt.hashpw(
        dto.password.encode("utf-8"),
        bcrypt.gensalt(
            rounds=int(
                environ.get("APP_HASH_ROUND", 12)
            )
        ),
    )

    with base.db.atomic():
        account_repository.insertOne(
            dto.username,
            hashed.decode("utf-8"),
            dto.email,
            dto.phone,
            dto.note,
        )

        account_id = (
            account_repository.getFields(
                dto.username,
                (account_repository.Account.id),
                False,
            )
        )[0]

        employee_code = generateEmployeeCode()

        profile_repository.insertOne(
            account_id,
            employee_code,
            dto.full_name,
        )


def generateEmployeeCode() -> str:
    """Loop and generate until the code is not duplicated."""
    _code = code.generateWithPrefix("EMP", 7)
    code_existed = profile_repository.checkCode(
        _code
    )

    while code_existed:
        _code = employee_code.generateWithPrefix(
            "EMP"
        )
        code_existed = (
            profile_repository.checkCode(_code)
        )
    return code
