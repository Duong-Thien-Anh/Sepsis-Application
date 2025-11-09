import logging
from fastapi import APIRouter


log = logging.getLogger("Account Controller")
router = APIRouter(
    prefix="/users", tags=["Accounts"]
)

# Re-import to trigger @router functions
from .getAll import getAll
from .signup import signup

__all__ = ["router"]
