"""
A sample Flask application using the Kerko blueprint.
"""

import os
import pathlib

import kerko
from flask import Flask, render_template
from flask_babel import get_locale
from kerko.config_helpers import config_update, load_toml, validate_config

from . import logging
from .config_helpers import KerkoAppModel, load_config_files
from .extensions import babel, bootstrap


def create_app() -> Flask:
    """
    Application factory.

    Explained here: http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)

    # Initialize app configuration with Kerko's defaults.
    config_update(app.config, kerko.DEFAULTS)

    # Update app configuration from TOML configuration file(s).
    load_config_files(app, os.environ.get('KERKOAPP_CONFIG_FILES'))

    # Update app configuration from environment variables.
    app.config.from_prefixed_env(prefix='KERKOAPP')

    # Perform validation checks on config.
    validate_config(app.config, 'kerko')
    validate_config(app.config, 'kerkoapp', KerkoAppModel)

    # Initialize the Composer object.
    app.config['kerko_composer'] = kerko.composer.Composer(app.config)

    # ----
    # If you are deriving your own custom application from KerkoApp, here is a
    # good place to alter the Composer object, perhaps adding facets.
    # ----

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    return app


def register_extensions(app: Flask) -> None:
    # Configure Babel to use both Kerko's translations and the app's.
    domain = ';'.join([kerko.TRANSLATION_DOMAIN, 'messages'])
    translation_directories = ';'.join(kerko.TRANSLATION_DIRECTORIES + ['translations'])
    babel.init_app(
        app,
        default_domain=domain,
        default_translation_directories=translation_directories,
    )

    logging.init_app(app)
    bootstrap.init_app(app)


def register_blueprints(app: Flask) -> None:
    # Setting `url_prefix` is required to distinguish the blueprint's static
    # folder route URL from the app's.
    app.register_blueprint(kerko.blueprint, url_prefix='/bibliography')


def register_errorhandlers(app: Flask) -> None:
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500.
        error_code = getattr(error, 'code', 500)
        context = {
            'locale': get_locale(),
        }
        return render_template(f'kerkoapp/{error_code}.html.jinja2', **context), error_code

    for errcode in [400, 403, 404, 500, 503]:
        app.errorhandler(errcode)(render_error)
