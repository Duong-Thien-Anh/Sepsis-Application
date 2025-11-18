from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any
from fastapi import HTTPException
from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    Field,
    TextField,
)


from .base import BaseModel


@dataclass
class UserExisted(HTTPException):
    msg: str = "Người dùng đã tồn tại."

    def __post_init__(self):
        super().__init__(
            status_code=400, detail=self.msg
        )


class Account(BaseModel):
    id = AutoField()
    username = CharField(max_length=100)
    password_hash = CharField()
    email = CharField()
    phone = CharField(max_length=20)
    role = CharField(max_length=50)
    status = CharField(max_length=50)
    created_date = DateField()
    last_login = DateTimeField()
    note = TextField()
    is_2fa_enabled = BooleanField()
    is_enabled = BooleanField()
    last_login_ip = CharField(max_length=100)
    login_method = CharField(max_length=50)

    class Meta:
        def table_function(_):
            return "Account"


def insertOne(
    username: str,
    password_hash: str,
    email: str,
    phone: str,
    note: str,
) -> None:
    _, created = Account.get_or_create(
        username=username,
        defaults={
            "password_hash": password_hash,
            "email": email,
            "phone": phone,
            "note": note,
        },
    )
    if not created:
        raise UserExisted()


def getAll() -> list[Account]:
    return list(Account.select())


def getFields(
    username_or_email: str,
    fields: tuple[Any, ...],
    is_email: bool,
) -> tuple[Any, ...]:
    """
    Get `fields` of an account by `username`.
    # Example:
    * `getFields(username, (Account.password_hash), False)`: get hashed password of an account by `username`.
    * `getFields(email, (Account.account_id, Account.password_hash), True)`: get id and hashed password of an account by `email`.
    """
    if not is_email:
        return (
            Account.select(fields)
            .where(
                Account.username
                == username_or_email
            )
            .tuples()
            .first()
        )
    else:
        return (
            Account.select(fields)
            .where(
                Account.email == username_or_email
            )
            .tuples()
            .first()
        )


def updateFields(
    usr: str,
    fields: Iterable[Field],
    values: Iterable[Any],
) -> None:
    """
    Update *only* the supplied fields.

    # Example
    ```python
    updateFields(
        (Account.password, Account.role),
        ("super_secret_password", "member")
    )
    ```
    """
    data: dict[Field, Any] = dict(
        zip(fields, values)
    )
    data = {
        field.name: value
        for field, value in zip(fields, values)
    }
    Account.update(**data).where(
        Account.username == usr
    ).execute()
    return
