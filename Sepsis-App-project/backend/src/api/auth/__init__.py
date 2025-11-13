import logging
from fastapi import APIRouter


log = logging.getLogger("Auth Controller")
router = APIRouter(prefix="/auth", tags=["Auth"])

# Re-import to trigger @router functions
from .signup import signup
from .login import login

__all__ = ["router"]
