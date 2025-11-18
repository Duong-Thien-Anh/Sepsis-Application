from datetime import datetime
import http
import logging
import re
from typing import Any
from fastapi import Security
from pydantic import BaseModel, field_validator


from ...utils.jwt import checkRole

from ...repositories import patient

from ..auth.signup import (
    InvalidEmailFormat,
    InvalidPhoneFormat,
)
from .. import VIETNAM_PHONE_REGEX, Gender
from ..response import Response

from . import router


class UpdatePatientDTO(BaseModel):
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


@router.put(
    "/{code}",
    dependencies=[
        Security(checkRole, scopes=["admin"])
    ],
)
def update(
    code: str,
    dto: UpdatePatientDTO,
) -> Response[None]:
    updateInternal(code, dto)
    return Response(
        http.HTTPStatus.OK,
        None,
        "Cập nhật hồ sơ bệnh nhân thành công!",
    )


def updateInternal(
    code: str, dto: UpdatePatientDTO
) -> None:
    logging.getLogger("uvicorn").info(dto)

    fields_to_update: list[str] = []
    values_to_update: list[Any] = []

    for attr, value in dto.model_dump().items():
        if attr == "code":
            continue

        if value is not None:
            try:
                peewee_field: str = attr
            except AttributeError as e:
                # silently skip unknown fields
                continue

            fields_to_update.append(peewee_field)
            values_to_update.append(value)

    patient.updateFields(
        code, fields_to_update, values_to_update
    )
    return
