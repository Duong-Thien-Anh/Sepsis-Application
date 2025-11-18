from datetime import datetime
import http
from fastapi import Security
from pydantic import BaseModel

from ...utils.jwt import checkRole
from ...repositories import patient
from ..response import Response
from . import router


class PatientResponse(BaseModel):
    code: str
    full_name: str
    date_of_birth: datetime | None
    gender: str | None
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
    photo_path: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


@router.get(
    "",
    dependencies=[
        Security(
            checkRole, scopes=["admin", "user"]
        )
    ],
)
def getAll() -> Response[list[PatientResponse]]:
    return Response(
        http.HTTPStatus.OK,
        getAllInternal(),
        "Lấy tất cả bệnh nhân thành công!",
    )


def getAllInternal() -> list[PatientResponse]:
    patients = patient.getAll()
    return [
        PatientResponse.model_validate(patient)
        for patient in patients
    ]
