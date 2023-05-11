import logging
from logging.config import dictConfig

from flask.logging import default_handler

# Set root logger to log to sys.stderr.
# Note: this must be set before the Flask app gets created.
dictConfig(
    {
        'version': 1,
        'formatters':
            {
                'default':
                    {
                        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                    }
            },
        'handlers':
            {
                'wsgi':
                    {
                        'class': 'logging.StreamHandler',
                        'stream': 'ext://flask.logging.wsgi_errors_stream',
                        'formatter': 'default'
                    }
            },
        'root':
            {
                'level': 'INFO',
                'handlers': ['wsgi']
            },
    }
)


def init_app(app):
    root = logging.getLogger()
    if app.config.get('LOGGING_HANDLER') == 'syslog':
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler(app.config.get('LOGGING_ADDRESS', '/dev/log'))
        syslog_handler.setFormatter(
            logging.Formatter(
                app.config.get(
                    'LOGGING_FORMAT', '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
                )
            )
        )
        app.logger.addHandler(syslog_handler)
        root.addHandler(syslog_handler)
    if 'LOGGING_LEVEL' in app.config:
        default_handler.setLevel(app.config['LOGGING_LEVEL'])
        app.logger.setLevel(app.config['LOGGING_LEVEL'])
        root.setLevel(app.config['LOGGING_LEVEL'])
