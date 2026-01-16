from typing import TypedDict


class HealthcheckTypeDict(TypedDict):
    status: str
    msg: str
