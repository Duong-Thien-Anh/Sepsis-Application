#! Mapping `exceptions` -> `responses`
from dataclasses import asdict
import http
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

# ---- Error Declaration ----
from .utils.jwt import Forbidden, InvalidToken
from .api.auth.signup import (
    InvalidEmailFormat,
    InvalidPhoneFormat,
)
from .api.auth.login import InvalidCredentials
from .api.response import Response
# ---------------------------

from . import app


@app.exception_handler(InvalidEmailFormat)
async def ief_error_handler(
    _: Request, exc: InvalidEmailFormat
) -> JSONResponse:
    return await response_400(exc.msg)


@app.exception_handler(InvalidPhoneFormat)
async def ipf_error_handler(
    _: Request, _1: InvalidPhoneFormat
) -> JSONResponse:
    return await response_400(
        "Số điện thoại không hợp lệ!\n"
        "• Phải bắt đầu bằng 0\n"
        "• Chỉ chứa số, dài 10‑11 chữ số\n"
        "• Ví dụ đúng:\n"
        " ├ Mobile: 0912345678, 0987654321\n"
        " └ Landline: 02812345678 (TP.HCM)\n"
        "• Hỗ trợ nhập: +84912345678, 084912345678, 0912 gue 345 678"
    )


@app.exception_handler(InvalidCredentials)
async def ic_error_handler(
    _: Request, exc: InvalidCredentials
) -> JSONResponse:
    return await response_400(exc.msg)


@app.exception_handler(InvalidToken)
async def it_error_handler(
    _: Request, exc: Forbidden
) -> JSONResponse:
    return await response_401(exc.msg)


@app.exception_handler(HTTPException)
async def http_error_handler(
    _: Request, exc: HTTPException
) -> JSONResponse:
    if exc.status_code == 403:
        return await response_403(exc.detail)
    elif exc.status_code == 401:
        return await response_401(exc.detail)
    elif exc.status_code == 400:
        return await response_400(exc.detail)
    else:
        return await response_500(exc.detail)


@app.exception_handler(Forbidden)
async def f_error_handler(
    _: Request, exc: Forbidden
) -> JSONResponse:
    return await response_403(exc.msg)


# Mapping our `Response` to `JSONResponse`
async def response_500(msg: str) -> JSONResponse:
    error_response = Response[None](
        status=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        data=None,
        message=msg,
    )
    return JSONResponse(
        status_code=error_response.status.value,
        content=asdict(error_response),
    )


async def response_400(msg: str) -> JSONResponse:
    error_response = Response[None](
        status=http.HTTPStatus.BAD_REQUEST,
        data=None,
        message=msg,
    )
    return JSONResponse(
        status_code=error_response.status.value,
        content=asdict(error_response),
    )


async def response_401(msg: str) -> JSONResponse:
    error_response = Response[None](
        status=http.HTTPStatus.UNAUTHORIZED,
        data=None,
        message=msg,
    )
    return JSONResponse(
        status_code=error_response.status.value,
        content=asdict(error_response),
    )


async def response_403(msg: str) -> JSONResponse:
    error_response = Response[None](
        status=http.HTTPStatus.FORBIDDEN,
        data=None,
        message=msg,
    )
    return JSONResponse(
        status_code=error_response.status.value,
        content=asdict(error_response),
    )
