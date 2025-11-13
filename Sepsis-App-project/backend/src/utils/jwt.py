from dataclasses import dataclass
import datetime
import logging
from os import environ
from typing import Annotated
from fastapi import Security, security
import jwt

from ..repositories import account


# ---- Exceptions ----
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
class Forbidden(Exception):
    """
    # Cases:
    * The token not found.
    * Token is wrong.
    * Invalid format.
    """

    msg: str


# ---------------------


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
    credentials: Annotated[
        security.HTTPAuthorizationCredentials,
        Security(security.HTTPBearer()),
    ],
) -> None:
    user = verify(credentials.credentials)
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
        raise Forbidden("Not enough permissions!")
