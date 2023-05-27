from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic import Extra, NonNegativeInt  # pylint: disable=no-name-in-module


class ProxyFixModel(BaseModel):

    class Config:
        extra = Extra.forbid

    enabled: bool = False
    x_for: NonNegativeInt = 1
    x_proto: NonNegativeInt = 1
    x_host: NonNegativeInt = 0
    x_port: NonNegativeInt = 0
    x_prefix: NonNegativeInt = 0


class KerkoAppModel(BaseModel):

    class Config:
        extra = Extra.forbid

    proxy_fix: Optional[ProxyFixModel]
