import secrets
import time
import jwt
import requests
from flask import Blueprint, abort, redirect, request, session, url_for
from . import eve

bp = Blueprint("auth", __name__)


@bp.route("/login")
def login():
    session["state"] = secrets.token_urlsafe(24)
    return redirect(eve.authorize_url(session["state"]))


@bp.route("/callback")
def callback():
    code = request.args.get("code")
    if not code or request.args.get("state") != session.get("state"):
        abort(400)
    try:
        cid, name = eve.verify_token(eve.exchange_code(code))
        member = eve.is_alliance_member(cid)
    except (requests.RequestException, jwt.PyJWTError, KeyError, ValueError):
        abort(502)
    if not member:
        session.clear()
        abort(403)
    nxt = session.get("next", "/guides")
    session.clear()  # prevent session fixation
    session.permanent = True
    session.update(character_id=cid, name=name, checked=time.time())
    return redirect(nxt if nxt.startswith("/") and not nxt.startswith("//") else "/guides")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))