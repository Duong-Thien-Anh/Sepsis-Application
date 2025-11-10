from dataclasses import asdict
from dataclasses import dataclass
import http
from fastapi import Request
from fastapi.responses import JSONResponse

from .api.response import Response
from . import app


@dataclass
class InvalidEmailFormat(Exception):
    msg: str


@dataclass
class InvalidPhoneFormat(Exception):
    pass


class UserExisted(Exception):
    pass


@app.exception_handler(UserExisted)
async def ue_error_handler(
    _: Request, _1: UserExisted
) -> JSONResponse:
    return await general_json_response(
        "The username existed!"
    )


@app.exception_handler(InvalidEmailFormat)
async def ief_error_handler(
    _: Request, exc: InvalidEmailFormat
) -> JSONResponse:
    return await general_json_response(exc.msg)


@app.exception_handler(InvalidPhoneFormat)
async def ipf_error_handler(
    _: Request, _1: InvalidPhoneFormat
) -> JSONResponse:
    return await general_json_response(
        "Số điện thoại không hợp lệ!\n"
        "• Phải bắt đầu bằng 0\n"
        "• Chỉ chứa số, dài 10-11 chữ số\n"
        "• Ví dụ đúng:\n"
        "  ├ Mobile: 0912345678, 0987654321\n"
        "  └ Landline: 02812345678 (TP.HCM)\n"
        "• Hỗ trợ nhập: +84912345678, 084912345678, 0912 345 678"
    )


async def general_json_response(
    msg: str,
) -> JSONResponse:
    error_response = Response[None](
        status=http.HTTPStatus.BAD_REQUEST,
        data=None,
        message=msg,
    )

    return JSONResponse(
        status_code=error_response.status.value,
        content=asdict(error_response),
    )
