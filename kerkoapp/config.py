from flask_babel import lazy_gettext as _


class BaseConfig:
    pass


class DevelopmentConfig(BaseConfig):

    def __init__(self):
        super().__init__()

        # pylint: disable=invalid-name

        self.LOGGING_LEVEL = 'DEBUG'
        # self.EXPLAIN_TEMPLATE_LOADING = True


class ProductionConfig(BaseConfig):

    def __init__(self):
        super().__init__()

        # pylint: disable=invalid-name

        self.LOGGING_LEVEL = 'WARNING'

        # FIXME: The following breaks on Windows
        # self.LOGGING_HANDLER = env.str('LOGGING_HANDLER', 'syslog')
        # self.LOGGING_ADDRESS = env.str('LOGGING_ADDRESS', '/dev/log')


CONFIGS = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
