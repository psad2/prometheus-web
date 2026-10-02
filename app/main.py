from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.app_errorhandler(403)
def forbidden(_):
    return render_template("error.html", msg="Access denied: you are not in the alliance."), 403


@bp.app_errorhandler(502)
@bp.app_errorhandler(503)
def upstream(_):
    return render_template("error.html", msg="EVE services are unavailable. Try again shortly."), 503