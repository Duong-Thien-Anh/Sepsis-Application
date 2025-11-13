from dataclasses import dataclass
import datetime
import logging
from os import environ
from typing import Annotated
from fastapi import Header, security
import jwt

from ..repositories import account


@dataclass
class InvalidToken(Exception):
    """
    # Cases:
    * The token not found.
    * Token is wrong.
    * Invalid format.
    """

    msg: str


@dataclass
class TokenPair:
    at: str
    rt: str


def create_token_pair(usr: str) -> TokenPair:
    payload = {
        "username": usr,
        "exp": datetime.datetime.today()
        + datetime.timedelta(hours=24),
    }

    key = environ.get("APP_SECRET")

    if key is None:
        raise Exception(
            "The secret application not found to encode JWT!"
        )

    at = jwt.encode(
        payload, key, algorithm="HS256"
    )
    return TokenPair(at, "")


def verify(token: str) -> str:
    try:
        key = environ.get("APP_SECRET")

        if key is None:
            raise Exception(
                "The secret application not found to decode JWT!"
            )

        decoded = jwt.decode(
            jwt=token, key=key, algorithms="HS256"
        )

        logging.getLogger("uvicorn").info(decoded)
        return decoded.get("username")
    except Exception as e:
        raise InvalidToken(
            "Your token is invalid!"
        )


async def checkRole(
    scopes: security.SecurityScopes,
    Authorization: Annotated[
        str | None, Header()
    ] = None,
) -> None:
    if Authorization == None:
        raise InvalidToken(
            "Your access token not found!"
        )

    if not Authorization.startswith("Bearer"):
        raise InvalidToken(
            "Your access token is invalid!"
        )

    token = Authorization.split(" ", 1)[1].strip()
    if len(token) < 2:
        raise InvalidToken(
            "Your access token is empty!"
        )

    user = verify(token)
    query = await account.getFields(
        user, (account.Account.role)
    )
    if query is None:
        raise InvalidToken(
            "Your access token is invalid!"
        )
    role = query[0]

    if (
        scopes.scopes
        and role not in scopes.scopes
    ):
        raise InvalidToken(
            "Not enough permissions!"
        )
