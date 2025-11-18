import http
from os import environ
import urllib.parse
from fastapi import HTTPException, Query
import requests


from ...repositories import account
from ...utils.jwt import (
    TokenPair,
    create_token_pair,
)

from ..response import Response

from .login import InvalidCredentials
from . import router


GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = environ.get(
    "GOOGLE_CLIENT_SECRET"
)

GOOGLE_REDIRECT_URL = (
    "http://localhost:"
    + environ.get("APP_PORT", "5000")
    + "/api/auth/google/callback"
)


@router.post("/google/login")
def googleLogin():
    params = {
        "response_type": "code",
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URL,
        "scope": "openid email profile",
    }
    query_string = urllib.parse.urlencode(params)
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"
    return {"login_url": auth_url}


def getUserInfo(code: str):
    token_url = (
        "https://oauth2.googleapis.com/token"
    )
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URL,
        "grant_type": "authorization_code",
    }
    token_response = requests.post(
        token_url, data=token_data
    )
    access_token = token_response.json().get(
        "access_token"
    )

    if not access_token:
        raise ValueError(
            "Failed to get access token"
        )

    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    user_response = requests.get(
        user_info_url, headers=headers
    )
    user_info = user_response.json()
    return user_info


@router.get("/google/callback")
def googleCallback(
    code: str = Query(...),
) -> Response[TokenPair]:
    if not code:
        raise HTTPException(
            status_code=400,
            detail="Error occurs when calling google callback, please contact with the developer team!",
        )

    user_info = getUserInfo(code)
    user = account.getFields(
        user_info["email"],
        (account.Account.username),
        True,
    )

    if user is None:
        raise InvalidCredentials(
            "Không tìm thấy người dùng!"
        )

    return Response(
        http.HTTPStatus.OK,
        data=create_token_pair(user),
        message="Đăng nhập thành công!",
    )
