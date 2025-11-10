import sys
from pathlib import Path


sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent)
)

from os import environ
from dotenv import load_dotenv

from . import app
from .api import account
from .repositories import base

# Load `.env` when the project is running
# in dev environement
if (
    environ.get("ENV") != "production"
    or Path(".env").exists()
):
    _ = load_dotenv(override=True)


base.BaseModel._meta.database.connect()

app.include_router(account.router, prefix="/api")
