from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Final
from . import app

fingerprint: dict[str, str] = {}


@dataclass
class LoginLimiter:
    @dataclass
    class Limit:
        to: datetime = (
            datetime.today()
            + timedelta(minutes=5)
        )
        times: int = 0

    list: dict[str, Limit] = field(
        default_factory=dict[str, Limit]
    )

    MAX_LOGIN_TIME: Final[int] = 5

    def increase(self, usr: str) -> None:
        usr_limit = self.list.get(usr)
        if (
            usr_limit != None
            and usr_limit.times
            < self.MAX_LOGIN_TIME
        ):
            usr_limit.times += 1
            usr_limit.to = (
                datetime.today()
                + timedelta(minutes=5)
            )

        return

    def isLimited(self, usr: str) -> bool:
        """Check if a account has reached MAX_LOGIN."""
        usr_limit = self.list.get(usr)

        if usr_limit == None:
            self.reset(usr)
            return False

        return (
            # the wrong login times has reached the max times.
            usr_limit.times >= self.MAX_LOGIN_TIME
            # check if the limit milestone is over
            and usr_limit.to > datetime.today()
        )

    def reset(self, usr: str) -> None:
        """Reset login times of an account."""
        self.list[usr] = self.Limit()
        return


login_limiter = LoginLimiter()


def getFingerprints(username: str) -> str | None:
    return fingerprint.get(username)


def setFingerprint(
    username: str, value: str
) -> None:
    fingerprint[username] = value
