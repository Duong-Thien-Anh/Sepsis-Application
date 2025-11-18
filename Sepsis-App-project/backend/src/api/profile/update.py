from datetime import date, datetime
import http
import logging
from typing import Any
from fastapi import Security
from pydantic import BaseModel


from ...utils.jwt import checkRole

from ...repositories import profile

from .. import Gender
from ..response import Response

from . import router


class UpdateProfileDTO(BaseModel):
    code: str
    full_name: str | None
    date_of_birth: datetime | None
    gender: Gender
    address: str | None
    position: str | None
    department: str | None
    start_date: date | None
    salary: int | None
    education_level: str | None
    license_number: str | None
    emergency_contact_name: str | None
    emergency_contact_relation: str | None
    emergency_contact_phone: str | None
    photo_path: str | None

    class Config:
        from_attributes = True


@router.put(
    "/{code}",
    dependencies=[
        Security(checkRole, scopes=["admin"])
    ],
)
def update(
    code: str,
    dto: UpdateProfileDTO,
) -> Response[None]:
    updateInternal(code, dto)
    return Response(
        http.HTTPStatus.OK,
        None,
        "Cập nhật hồ sơ thành công!",
    )


def updateInternal(
    code: str, dto: UpdateProfileDTO
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

    profile.updateFields(
        code, fields_to_update, values_to_update
    )
    return
