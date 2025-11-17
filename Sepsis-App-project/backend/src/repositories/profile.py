from dataclasses import dataclass
from fastapi import HTTPException
from peewee import (
    CharField,
    DateField,
    DecimalField,
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


class Employee(BaseModel):
    code = CharField(primary_key=True)
    account_id = ForeignKeyField(
        Account, field=Account.id
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
            return "Employee"


def checkCode(code: str) -> bool:
    return (
        Employee.select()
        .where(Employee.code == code)
        .exists()
    )


def get(usr: str) -> Employee:
    return (
        Employee.select()
        .join(Account)
        .where(Account.username == usr)
        .first()
    )


async def insertOne(
    account_id: int,
    employee_code: str,
    full_name: str,
) -> None:
    _, created = Employee.get_or_create(
        account_id=account_id,
        defaults={
            "employee_code": employee_code,
            "full_name": full_name,
        },
    )

    if not created:
        raise ProfileExisted()
    return
