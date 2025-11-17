import logging
from fastapi import APIRouter


router = APIRouter(
    prefix="/profile", tags=["Profile"]
)

# Re-import to trigger @router functions
from .get import me


__all__ = ["router"]
