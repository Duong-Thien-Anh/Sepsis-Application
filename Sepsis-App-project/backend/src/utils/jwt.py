#! Each account should be accessed by only 1 device
from dataclasses import dataclass
import datetime
import logging
from os import environ
import os
from typing import Annotated
from fastapi import Security, security
import jwt

from ..state import (
    getFingerprints,
    setFingerprint,
)

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
    fp = os.urandom(32).hex()
    setFingerprint(usr, fp)

    payload = {
        "username": usr,
        "fingerprint": fp,
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
    key = environ.get("APP_SECRET")

    if key is None:
        raise Exception(
            "The secret application not found to decode JWT!"
        )

    decoded = jwt.decode(
        jwt=token, key=key, algorithms="HS256"
    )
    usr = decoded.get("username")
    fp = decoded.get("fingerprint")
    exp = datetime.datetime.fromtimestamp(
        int(decoded.get("exp"))
    )

    if (
        getFingerprints(usr) is None
        or getFingerprints(usr) != fp
    ):
        raise InvalidToken(
            "Your token is invalid!"
        )

    if exp < datetime.datetime.now():
        raise InvalidToken(
            "Your token is expired!"
        )

    return usr


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
