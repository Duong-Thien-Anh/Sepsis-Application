from fastapi import APIRouter


router = APIRouter(
    prefix="/patients", tags=["Patients"]
)

# Re-import to trigger @router functions
from .get import getAll
from .insert import insert
from .update import update


__all__ = ["router"]
