"""
Instantiate extensions.

Each extension is initialized by the create_app factory of the app module.
"""

from flask_babel import Babel
from flask_bootstrap import Bootstrap4

babel = Babel()
bootstrap = Bootstrap4()
