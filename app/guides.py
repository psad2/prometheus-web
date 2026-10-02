import markdown
from flask import Blueprint, abort, render_template
from . import config as c
from .decorators import member_required

bp = Blueprint("guides", __name__, url_prefix="/guides")


def list_guides():
    out = []
    for p in sorted(c.GUIDES_DIR.glob("*.md")):
        lines = p.read_text(encoding="utf-8").splitlines()
        title = lines[0].lstrip("# ").strip() if lines else ""
        out.append({"slug": p.stem, "title": title or p.stem})
    return out


@bp.route("/")
@member_required
def index():
    return render_template("guides.html", guides=list_guides())


@bp.route("/<slug>")
@member_required
def view(slug):
    match = next((g for g in list_guides() if g["slug"] == slug), None)  # allow-list, no path traversal
    if not match:
        abort(404)
    text = (c.GUIDES_DIR / f"{slug}.md").read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code"])
    return render_template("guide.html", title=match["title"], body=body)