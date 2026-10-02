from flask import Flask
from . import config as c


def create_app():
    app = Flask(__name__, template_folder="../templates")
    app.config.update(
        SECRET_KEY=c.SECRET_KEY,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=c.COOKIE_SECURE,
        PERMANENT_SESSION_LIFETIME=8 * 3600,
    )
    from . import main, auth, guides, calculator
    for module in (main, auth, guides, calculator):
        app.register_blueprint(module.bp)
    return app