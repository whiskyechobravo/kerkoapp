import errno
import sys

from flask import redirect, url_for
from kerko.config_helpers import config_get

from kerkoapp import create_app

try:
    app = create_app()
except RuntimeError as e:
    print(e, file=sys.stderr)  # noqa: T201
    sys.exit(errno.EINTR)  # This should make the WSGI server exit as well.


@app.route("/")
def home():
    return redirect(url_for("kerko.search"))


try:
    proxy_fix_config = config_get(app.config, "kerkoapp.proxy_fix")
except KeyError:
    pass
else:
    if proxy_fix_config.get("enabled"):
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(
            app.wsgi_app,
            **{kwarg: value for kwarg, value in proxy_fix_config.items() if kwarg != "enabled"},
        )


@app.shell_context_processor
def make_shell_context():
    """Return context dict for a shell session, giving access to variables."""
    return dict(app=app)
