from . import app


fingerprint: dict[str, str] = {}


def getFingerprints(username: str) -> str | None:
    return fingerprint.get(username)


def setFingerprint(
    username: str, value: str
) -> None:
    fingerprint[username] = value
