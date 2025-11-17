import sys
from pathlib import Path


sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent)
)

from fastapi.middleware.cors import CORSMiddleware
from os import environ
from dotenv import load_dotenv

from . import app, error
from .api import account, auth, profile
from .repositories import base

# Load `.env` when the project is running
# in dev environement
if (
    environ.get("ENV") != "production"
    or Path(".env").exists()
):
    _ = load_dotenv(override=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=environ.get(
        "CLIENT_URL", "client_url"
    ),
    allow_methods=["*"],
    allow_headers=["*"],
)

base.BaseModel._meta.database.connect()

app.include_router(account.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
