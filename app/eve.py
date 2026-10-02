"""EVE SSO + ESI helpers. No Flask imports, so this is easy to test and reuse."""
from urllib.parse import urlencode
import jwt
import requests
from jwt import PyJWKClient
from . import config as c

_jwks = PyJWKClient(f"{c.SSO_URL}/oauth/jwks")


def authorize_url(state):
    params = {"response_type": "code", "redirect_uri": c.CALLBACK_URL,
              "client_id": c.CLIENT_ID, "state": state}  # no scopes: identity only
    return f"{c.SSO_URL}/v2/oauth/authorize?{urlencode(params)}"


def exchange_code(code):
    r = requests.post(f"{c.SSO_URL}/v2/oauth/token",
                      data={"grant_type": "authorization_code", "code": code},
                      auth=(c.CLIENT_ID, c.CLIENT_SECRET),
                      headers={"User-Agent": c.USER_AGENT}, timeout=10)
    r.raise_for_status()
    return r.json()["access_token"]


def verify_token(access_token):
    """Validate signature/expiry/audience/issuer; return (character_id, name)."""
    key = _jwks.get_signing_key_from_jwt(access_token).key
    claims = jwt.decode(access_token, key, algorithms=["RS256"], audience="EVE Online",
                        options={"require": ["exp", "iss", "sub"]})
    if claims["iss"] not in (c.SSO_URL, "login.eveonline.com"):
        raise jwt.InvalidIssuerError("bad issuer")
    return int(claims["sub"].split(":")[-1]), claims["name"]


def get_affiliation(character_id):
    """Public ESI endpoint (no scope). Returns dict with alliance_id/corporation_id or None."""
    r = requests.post(f"{c.ESI_URL}/characters/affiliation/", json=[character_id],
                      headers={"User-Agent": c.USER_AGENT}, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data[0] if data else None


def is_alliance_member(character_id):
    aff = get_affiliation(character_id)
    return bool(aff) and aff.get("alliance_id") == c.ALLIANCE_ID