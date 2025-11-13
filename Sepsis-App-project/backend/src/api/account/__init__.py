import logging
from fastapi import APIRouter


log = logging.getLogger("Account Controller")
router = APIRouter(
    prefix="/users", tags=["Accounts"]
)

# Re-import to trigger @router functions
from .get import getAll

__all__ = ["router"]
