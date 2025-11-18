from datetime import date, datetime
import http
from typing import Annotated

from fastapi import (
    Depends,
    HTTPException,
    Security,
)
from pydantic import BaseModel

from .. import Gender

from ...utils.jwt import checkRole, getCurrentUser
from ...repositories import profile
from ..response import Response

from . import router


class ProfileResponse(BaseModel):
    employee_code: str
    account_id: int
    full_name: str
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
    profile_m = profile.get(usr, False)
    if profile_m is None:
        raise HTTPException(
            400, "The user profile not found!"
        )
    return ProfileResponse.model_validate(
        profile_m
    )


@router.get(
    "/{code}",
    dependencies=[
        Security(checkRole, scopes=["admin"])
    ],
)
def getByEmployeeCode(
    code: str,
) -> Response[ProfileResponse]:
    return Response(
        http.HTTPStatus.OK,
        getByEmployeeCodeInternal(code),
        "Lấy hồ sơ thành công!",
    )


def getByEmployeeCodeInternal(
    code: str,
) -> ProfileResponse:
    profile_m = profile.get(code, True)
    if profile_m is None:
        raise HTTPException(
            400,
            "Không tìm thấy hồ sơ người dùng!",
        )
    return ProfileResponse.model_validate(
        profile_m
    )


@router.get(
    "",
    dependencies=[
        Security(checkRole, scopes=["admin"])
    ],
)
def getAll() -> Response[list[ProfileResponse]]:
    return Response(
        http.HTTPStatus.OK,
        getAllInternal(),
        "Lấy hồ sơ thành công!",
    )


def getAllInternal() -> list[ProfileResponse]:
    profiles = profile.getAll()
    return [
        ProfileResponse.model_validate(profile)
        for profile in profiles
    ]
