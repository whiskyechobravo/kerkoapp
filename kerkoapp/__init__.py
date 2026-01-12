"""
A sample Flask application using the Kerko blueprint.
"""

import os

import kerko
from flask import Flask, render_template
from flask_babel import get_locale
from kerko.config_helpers import config_update, parse_config

from . import logging
from .config_helpers import KerkoAppModel, load_config_files
from .extensions import babel, bootstrap, plugin_manager


def create_app() -> Flask:
    """
    Application factory.

    Explained here: http://flask.pocoo.org/docs/patterns/appfactories/
    """
    try:
        app = Flask(__name__, instance_path=os.environ.get("KERKOAPP_INSTANCE_PATH"))
    except ValueError as e:
        msg = f"Unable to initialize the application. {e}"
        raise RuntimeError(msg) from e

    # Initialize app configuration with Kerko's defaults.
    config_update(app.config, kerko.DEFAULTS)

    # Update app configuration from TOML configuration file(s).
    load_config_files(app, os.environ.get("KERKOAPP_CONFIG_FILES"))

    # Update app configuration from environment variables.
    app.config.from_prefixed_env(prefix="KERKOAPP")

    # Validate configuration and save its parsed version.
    parse_config(app.config)

    # Validate extra configuration model and save its parsed version.
    if app.config.get("kerkoapp"):
        parse_config(app.config, "kerkoapp", KerkoAppModel)

    # Initialize the Composer object.
    app.config["kerko_composer"] = kerko.composer.Composer(app.config)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    return app


def register_extensions(app: Flask) -> None:
    # Initialize Babel to use translations from both Kerko and the app. Config
    # parameters BABEL_DOMAIN and BABEL_TRANSLATION_DIRECTORIES may override
    # these defaults. When multiple translation directories are used, a domain
    # MUST be specified for each directory. Thus, both lists must have the same
    # number of items (separated by semi-colons).
    domain = f"{kerko.TRANSLATION_DOMAIN};messages"
    directories = f"{kerko.TRANSLATION_DIRECTORY};translations"
    babel.init_app(
        app,
        default_domain=domain,
        default_translation_directories=directories,
    )

    logging.init_app(app)
    bootstrap.init_app(app)
    plugin_manager.init_app(app)


def register_blueprints(app: Flask) -> None:
    # Setting `url_prefix` is required to distinguish the blueprint's static
    # folder route URL from the app's.
    app.register_blueprint(kerko.make_blueprint(), url_prefix="/bibliography")


def register_errorhandlers(app: Flask) -> None:
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500.
        error_code = getattr(error, "code", 500)
        context = {
            "locale": get_locale(),
        }
        return render_template(f"kerkoapp/{error_code}.html.jinja2", **context), error_code

    for errcode in [400, 403, 404, 500, 503]:
        app.errorhandler(errcode)(render_error)
