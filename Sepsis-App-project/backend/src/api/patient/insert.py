from datetime import datetime
import http
import re
from fastapi import Security
from pydantic import BaseModel, field_validator


from ...utils import code

from .. import VIETNAM_PHONE_REGEX, Gender

from ..auth.signup import (
    InvalidEmailFormat,
    InvalidPhoneFormat,
)

from ...utils.jwt import checkRole
from ...repositories import patient
from ..response import Response
from . import router


class InsertPatientResponse(BaseModel):
    full_name: str
    date_of_birth: datetime | None
    gender: Gender
    phone: str | None
    email: str | None
    address: str | None
    blood_type: str | None
    height_cm: int | None
    weight_kg: int | None
    medical_history: str | None
    emergency_contact_name: str | None
    emergency_contact_relation: str | None
    emergency_contact_phone: str | None

    class Config:
        from_attributes = True

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


@router.post(
    "",
    dependencies=[
        Security(
            checkRole, scopes=["admin", "user"]
        )
    ],
)
def insert(
    dto: InsertPatientResponse,
) -> Response[None]:
    insertInternal(dto)
    return Response(
        http.HTTPStatus.OK,
        None,
        "Tạo hồ sơ bệnh nhân thành công!",
    )


def insertInternal(
    dto: InsertPatientResponse,
) -> None:
    patient.insertOne(
        code.generateWithPrefix("PAT", 12),
        dto.full_name,
        dto.date_of_birth,
        dto.gender,
        dto.phone,
        dto.email,
        dto.address,
        dto.blood_type,
        dto.height_cm,
        dto.weight_kg,
        dto.medical_history,
        dto.emergency_contact_name,
        dto.emergency_contact_relation,
        dto.emergency_contact_phone,
    )
    return
