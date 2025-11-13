from typing import Any
from peewee import (
    AutoField,
    BitField,
    CharField,
    DateField,
    DateTimeField,
    Field,
    OperationalError,
    TextField,
)

from ..error import (
    InvalidEmailFormat,
    UserExisted,
)

from .base import BaseModel
from datetime import date, datetime


class Account(BaseModel):
    account_id = AutoField()
    username = CharField(max_length=100)
    password_hash = CharField()
    full_name = CharField()
    email = CharField()
    phone = CharField(max_length=20)
    role = CharField(max_length=50)
    status = CharField(max_length=50)
    created_date = DateField()
    last_login = DateTimeField()
    note = TextField()
    is_2fa_enabled = BitField()
    last_login_ip = CharField(max_length=100)
    login_method = CharField(max_length=50)

    class Meta:
        def table_function(_):
            return "Account"


async def insertOne(
    username: str,
    password_hash: str,
    full_name: str,
    email: str,
    phone: str,
    note: str,
) -> None:
    try:
        Account.create(
            username=username,
            password_hash=password_hash,
            full_name=full_name,
            email=email,
            phone=phone,
            status="new",
            role="member",
            created_date=date.today(),
            last_login=datetime.today(),
            note=note,
            last_login_ip="1.1.1.1",
            is_2fa_enabled=False,
            login_method="normal",
        )
    except OperationalError as e:
        # TODO: handle error
        print(f"Error code: {e.args[0]}")
        print(f"Error message: {e.args[1]}")


async def getAll() -> list[Account]:
    return list(Account.select())


async def getFields(
    username: str, fields: tuple[Any, ...]
) -> tuple[Any, ...]:
    """
    Get `fields` of an account by `username`.
    # Example:
    * `getOptional(username, (Account.password_hash))`: get hashed password of an account.
    * `getOptional(username, (Account.account_id, Account.password_hash))`: get id and hashed password of an account.
    """
    return (
        Account.select(fields)
        .where(Account.username == username)
        .tuples()
        .first()
    )
