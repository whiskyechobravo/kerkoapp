from environs import Env
from flask import redirect, url_for

from app import create_app

env = Env()  # pylint: disable=invalid-name
env.read_env()

app = create_app(env.str('FLASK_ENV'))  # pylint: disable=invalid-name


@app.route('/')
def home():
    return redirect(url_for('kerko.search'))


if app.config['PROXY_FIX']:
    # CAUTION: It is a security issue to use this middleware in a non-proxy
    # setup because it will blindly trust the incoming headers which might be
    # forged by malicious clients.
    # Ref: https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/#proxy-setups
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)


@app.shell_context_processor
def make_shell_context():
    """Return context dict for a shell session, giving access to variables."""
    return dict(app=app)
