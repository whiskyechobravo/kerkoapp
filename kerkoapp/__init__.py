"""
A sample Flask application using the Kerko blueprint.
"""

import pathlib

import kerko
from flask import Flask, render_template
from flask_babel import Domain, get_locale

from . import logging
from .config import CONFIGS
from .extensions import babel, bootstrap


def create_app():
    """
    Application factory.

    Explained here: http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(CONFIGS['development' if app.config['DEBUG'] else 'production']())
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
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


def register_blueprints(app):
    # Setting `url_prefix` is required to distinguish the blueprint's static
    # folder route URL from the app's.
    app.register_blueprint(kerko.blueprint, url_prefix='/bibliography')


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500.
        error_code = getattr(error, 'code', 500)
        context = {
            'locale': get_locale(),
        }
        return render_template(f'kerkoapp/{error_code}.html.jinja2', **context), error_code

    for errcode in [400, 403, 404, 500, 503]:
        app.errorhandler(errcode)(render_error)
