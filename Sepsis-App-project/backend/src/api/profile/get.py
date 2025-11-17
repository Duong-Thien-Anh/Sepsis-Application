from datetime import date, datetime
import http
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from ...utils.jwt import getCurrentUser
from ...repositories import profile
from ..response import Response

from . import router


class ProfileResponse(BaseModel):
    code: str
    full_name: str
    date_of_birth: datetime
    gender: str | None
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


@router.get("/me")
def me(
    curr_usr: Annotated[
        str, Depends(getCurrentUser)
    ],
) -> Response[ProfileResponse]:
    return Response(
        http.HTTPStatus.OK,
        meInternal(curr_usr),
        "Lấy hồ sơ thành công!",
    )


def meInternal(usr: str) -> ProfileResponse:
    profile_m = profile.get(usr)
    return ProfileResponse.model_validate(
        profile_m
    )
