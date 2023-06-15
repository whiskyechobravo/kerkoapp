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


def load_config_files(app: Flask, path_spec: Optional[str]):
    """
    Load configuration files from a semicolon-separated list of paths.

    Paths may be absolute or relative. Relative paths are resolved from the
    app's instance path, which is determined by Flask.

    See https://flask.palletsprojects.com/en/2.3.x/config/#instance-folders.

    If a file is not found at the given resolved path, it is searched by
    traversing directories up.

    The files are loaded in the specified order, the configuration from each
    file getting merged into the previously known configuration. If a variable
    is already set, its value is overwritten by the one from the later file.

    The default `path_spec` is `"config.toml;instance.toml;.secrets.toml"`.
    """
    found = False
    tried = []
    if not path_spec:
        path_spec = "config.toml;instance.toml;.secrets.toml"
    for path_item in path_spec.split(';'):
        try_parents = [pathlib.Path(app.instance_path)]
        try_parents += pathlib.Path(app.instance_path).parents
        while try_parents:
            path = try_parents.pop(0) / path_item.strip()
            if path.is_file():
                config_update(app.config, load_toml(path, verbose=True))
                found = True
                break
            else:
                tried.append(str(path))
    if not found:
        raise RuntimeError(
            "No configuration found. The following paths were unsuccessfully "
            "tried:\n{}".format('\n'.join(tried))
        )
