from enum import StrEnum
import re

VIETNAM_PHONE_REGEX = re.compile(
    r"^0[1-9][0-9]{8,9}$"
)


class Gender(StrEnum):
    Male = "Male"
    Female = "Female"
    Other = "Other"
