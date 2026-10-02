import json
from flask import Blueprint, render_template, request
from . import config as c
from .decorators import member_required

bp = Blueprint("calculator", __name__, url_prefix="/calculator")


class QuoteError(Exception):
    """Validation error that is safe to show to the user."""


def quote(route, volume, collateral):
    if volume <= 0 or collateral < 0:
        raise QuoteError("Volume must be positive and collateral cannot be negative.")
    if volume > route["max_volume"]:
        raise QuoteError(f"Max volume on this route is {route['max_volume']:,} m³.")
    if collateral > route["max_collateral"]:
        raise QuoteError(f"Max collateral on this route is {route['max_collateral']:,} ISK.")
    vol_fee = volume * route["rate_per_m3"]
    col_fee = collateral * route["collateral_pct"] / 100
    return {"route": route["name"], "vol_fee": vol_fee, "col_fee": col_fee, "total": vol_fee + col_fee}


@bp.route("/", methods=["GET", "POST"])
@member_required
def index():
    routes = json.loads(c.RATES_FILE.read_text())["routes"]
    result = error = None
    if request.method == "POST":
        try:
            route = routes[int(request.form["route"])]
            result = quote(route, float(request.form["volume"]), float(request.form["collateral"]))
        except QuoteError as e:
            error = str(e)
        except (ValueError, KeyError, IndexError):
            error = "Please check your inputs."
    return render_template("calculator.html", routes=routes, result=result, error=error)