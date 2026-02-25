import logging
from logging.config import dictConfig

from flask.logging import default_handler

from .extensions import plugin_manager

DEFAULT_LOGGING_FORMAT = "[%(asctime)s] %(levelname)s in %(name)s - %(message)s"

# Set root logger to log to sys.stderr.
# Note: this must be set before the Flask app gets created.
dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": DEFAULT_LOGGING_FORMAT,
            },
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            },
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)


def init_app(app):
    if app.config["DEBUG"]:
        # Set DEBUG logging level for registered plugins.
        for plugin in plugin_manager.get_plugins():
            plugin_module = plugin.__module__
            plugin_logger = logging.getLogger(plugin_module)
            plugin_logger.setLevel(logging.DEBUG)
    else:
        # Override logging level for httpx to reduce noise.
        logging.getLogger("httpx").setLevel(logging.WARNING)

    root = logging.getLogger()
    if app.config.get("LOGGING_HANDLER") == "syslog":
        from logging.handlers import SysLogHandler

        syslog_handler = SysLogHandler(app.config.get("LOGGING_ADDRESS", "/dev/log"))
        syslog_handler.setFormatter(
            logging.Formatter(app.config.get("LOGGING_FORMAT", DEFAULT_LOGGING_FORMAT))
        )
        root.addHandler(syslog_handler)

    if "LOGGING_LEVEL" in app.config:
        # Set logging level from config.
        default_handler.setLevel(app.config["LOGGING_LEVEL"])
        app.logger.setLevel(app.config["LOGGING_LEVEL"])
        root.setLevel(app.config["LOGGING_LEVEL"])
