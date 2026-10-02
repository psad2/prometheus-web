import time
from functools import wraps
import requests
from flask import abort, redirect, request, session, url_for
from . import config as c, eve


def member_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        cid = session.get("character_id")
        if not cid:
            session["next"] = request.path
            return redirect(url_for("auth.login"))
        if time.time() - session.get("checked", 0) > c.RECHECK_SECONDS:
            try:
                ok = eve.is_alliance_member(cid)
            except requests.RequestException:
                abort(503)
            if not ok:
                session.clear()
                abort(403)
            session["checked"] = time.time()
        return f(*args, **kwargs)
    return wrapper