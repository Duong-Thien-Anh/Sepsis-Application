from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any
from fastapi import HTTPException
from peewee import (
    CharField,
    DateField,
    DecimalField,
    Field,
    ForeignKeyField,
    TextField,
)

from .account import Account
from .base import BaseModel


@dataclass
class ProfileExisted(HTTPException):
    msg: str = "Hồ sơ người dùng đã tồn tại."

    def __post_init__(self):
        super().__init__(
            status_code=400, detail=self.msg
        )


class Profile(BaseModel):
    employee_code = CharField(primary_key=True)
    account_id = ForeignKeyField(
        Account, field=Account.id, lazy_load=False
    )
    full_name = CharField()
    date_of_birth = DateField()
    gender = CharField()
    address = TextField()
    position = CharField()
    department = CharField()
    start_date = DateField()
    salary = DecimalField()
    education_level = CharField()
    license_number = CharField()
    emergency_contact_name = CharField()
    emergency_contact_relation = CharField()
    emergency_contact_phone = CharField()
    photo_path = CharField()

    class Meta:
        def table_function(_):
            return "Profile"


def checkCode(code: str) -> bool:
    return (
        Profile.select()
        .where(Profile.employee_code == code)
        .exists()
    )


def get(
    usr_or_code: str, is_code: bool
) -> Profile:
    if not is_code:
        return (
            Profile.select()
            .join(Account)
            .where(
                Account.username == usr_or_code
            )
            .first()
        )
    else:
        return (
            Profile.select()
            .where(
                Profile.employee_code
                == usr_or_code
            )
            .first()
        )


def insertOne(
    account_id: int,
    employee_code: str,
    full_name: str,
) -> None:
    _, created = Profile.get_or_create(
        account_id=account_id,
        defaults={
            "employee_code": employee_code,
            "full_name": full_name,
        },
    )

    if not created:
        raise ProfileExisted()
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
        (Profile.day_of_birth, Profile.position),
        ("11/02/1999", "doctor")
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
    Profile.update(**data).where(
        Profile.employee_code == code
    ).execute()
    return


def getAll() -> list[Profile]:
    return Profile.select()
