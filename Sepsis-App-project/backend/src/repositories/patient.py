from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from fastapi import HTTPException
from peewee import (
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    ForeignKeyField,
    IntegerField,
    TextField,
)

from ..api import Gender

from .base import BaseModel


@dataclass
class PatientExisted(HTTPException):
    msg: str = "Hồ sơ bệnh nhân đã tồn tại."

    def __post_init__(self):
        super().__init__(
            status_code=400, detail=self.msg
        )


class Patient(BaseModel):
    code = CharField(primary_key=True)
    full_name = CharField()
    date_of_birth = DateField()
    gender = CharField()
    phone = CharField()
    email = CharField()
    address = TextField()
    blood_type = CharField()
    height_cm = IntegerField()
    weight_kg = DecimalField()
    medical_history = CharField()
    emergency_contact_name = CharField()
    emergency_contact_relation = CharField()
    emergency_contact_phone = CharField()
    photo_path = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        def table_function(_):
            return "Patient"


def get(code: str) -> Patient:
    return (
        Patient.select()
        .where(Patient.code == code)
        .first()
    )


def insertOne(
    code: str,
    full_name: str,
    date_of_birth: datetime | None,
    gender: Gender,
    phone: str | None,
    email: str | None,
    address: str | None,
    blood_type: str | None,
    height_cm: int | None,
    weight_kg: int | None,
    medical_history: str | None,
    emergency_contact_name: str | None,
    emergency_contact_relation: str | None,
    emergency_contact_phone: str | None,
) -> None:
    _, created = Patient.get_or_create(
        code=code,
        defaults={
            "full_name": full_name,
            "gender": gender,
            "date_of_birth": date_of_birth,
            "phone": phone,
            "email": email,
            "address": address,
            "blood_type": blood_type,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "medical_history": medical_history,
            "emergency_contact_name": emergency_contact_name,
            "emergency_contact_relation": emergency_contact_relation,
            "emergency_contact_phone": emergency_contact_phone,
        },
    )

    if not created:
        raise PatientExisted()
    return


def updateFields(
    code: str,
    fields: Iterable[str],
    values: Iterable[Any],
) -> None:
    """
    Update *only* the supplied fields.

    # Example
    ```python
    updateFields(
        ("day_of_birth", "full_name"),
        ("11/02/1999", "Hoang")
    )
    ```
    """
    data: dict[str, Any] = dict(
        zip(fields, values)
    )
    data = {
        field: value
        for field, value in zip(fields, values)
    }
    Patient.update(**data).where(
        Patient.code == code
    ).execute()
    return


def getAll() -> list[Patient]:
    return Patient.select()
