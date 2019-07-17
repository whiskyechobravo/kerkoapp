"""
Instanciate extensions.

Each extension is initialized by the create_app factory of the app module.
"""
# pylint: disable=invalid-name

import pathlib

from flask_babelex import Babel, Domain
from flask_bootstrap import Bootstrap

babel_domain = Domain(pathlib.Path(__file__).parent / 'translations')
babel = Babel(default_domain=babel_domain)
bootstrap = Bootstrap()
