def init_app(app):
    if app.config['LOGGING_HANDLER'] == 'syslog':
        # Log messages to syslogd.
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler(app.config['LOGGING_ADDRESS'])
        syslog_handler.setLevel(app.config['LOGGING_LEVEL'])
        syslog_handler.setFormatter(logging.Formatter(app.config['LOGGING_FORMAT']))
        app.logger.addHandler(syslog_handler)
