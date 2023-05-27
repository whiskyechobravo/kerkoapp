import pathlib
from typing import Optional

from flask import Flask
from kerko.config_helpers import config_update, load_toml
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


def load_config_files(app: Flask, path_spec: str):
    """
    Load configuration files from a semicolon-separated list of paths.

    The configuration from each file will be merged into the known
    configuration. When file refers to a setting that was already set by a
    previous file, it overrides the previous value.

    If no path is specified, try loading `config.toml` under the application's
    root path.
    """
    paths = [pathlib.Path(app.root_path) / p.strip() for p in path_spec.split(';') if p.strip()]
    if not paths:
        paths = [pathlib.Path(app.root_path) / 'config.toml']  # Default path.
    for path in paths:
        config_update(app.config, load_toml(path))
