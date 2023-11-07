import pathlib
from typing import Optional

from flask import Flask
from kerko.config_helpers import config_update, load_toml
from pydantic import (
    BaseModel,
    Extra,
    NonNegativeInt,
)


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


def load_config_files(app: Flask, path_spec: Optional[str]):
    """
    Load configuration files from a semicolon-separated list of paths.

    The configuration files are loaded in the specified order, the parameters
    from each file getting merged into the previously known configuration. If a
    given parameter was already set, its value is overwritten by the one from
    the later file.

    The default `path_spec` is `"config.toml;instance.toml;.secrets.toml"`.

    Paths may be absolute or relative. Relative paths are resolved from the
    current working directory. If the file is not found there, it is searched by
    traversing the directories up. If the root directory is reached and the file
    still not found, the same search is reapplied, this time starting from the
    application's instance directory.
    """
    cwd_parents = [pathlib.Path.cwd(), *pathlib.Path.cwd().parents]
    instance_path = pathlib.Path(app.instance_path)
    instance_parents = [instance_path, *instance_path.parents]
    try_parents = cwd_parents + [p for p in instance_parents if p not in cwd_parents]
    if not path_spec:
        path_spec = "config.toml;instance.toml;.secrets.toml"
    for path_item in path_spec.split(";"):
        for parent in try_parents:
            path = parent / path_item.strip()
            if path.is_file():
                config_update(app.config, load_toml(path, verbose=app.config["DEBUG"]))
                break
