import logging
from typing import Annotated
from fastapi import Header, security

from ..utils import jwt
from ..repositories import account

log = logging.getLogger("uvicorn")


async def checkRole(
    scopes: security.SecurityScopes,
    Authorization: Annotated[
        str | None, Header()
    ] = None,
) -> None:
    if Authorization == None:
        raise jwt.InvalidToken(
            "Your access token not found!"
        )

    if not Authorization.startswith("Bearer"):
        raise jwt.InvalidToken(
            "Your access token is invalid!"
        )

    token = Authorization.split(" ", 1)[1].strip()
    if len(token) < 2:
        raise jwt.InvalidToken(
            "Your access token is empty!"
        )

    user = jwt.verify(token)
    query = await account.getFields(
        user, (account.Account.role)
    )
    if query is None:
        raise jwt.InvalidToken(
            "Your access token is invalid!"
        )
    role = query[0]

    if (
        scopes.scopes
        and role not in scopes.scopes
    ):
        raise jwt.InvalidToken(
            "Not enough permissions!"
        )
