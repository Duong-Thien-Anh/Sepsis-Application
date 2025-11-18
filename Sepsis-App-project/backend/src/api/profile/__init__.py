import logging
from fastapi import APIRouter


router = APIRouter(
    prefix="/profile", tags=["Profile"]
)

# Re-import to trigger @router functions
from .get import me
from .update import update


__all__ = ["router"]
