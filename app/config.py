import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ["SECRET_KEY"]
CLIENT_ID = os.environ["EVE_CLIENT_ID"]
CLIENT_SECRET = os.environ["EVE_CLIENT_SECRET"]
CALLBACK_URL = os.environ["EVE_CALLBACK_URL"]
ALLIANCE_ID = int(os.environ["ALLIANCE_ID"])
USER_AGENT = os.getenv("ESI_USER_AGENT", "alliance-site")
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "1") == "1"

SSO_URL = "https://login.eveonline.com"
ESI_URL = "https://esi.evetech.net/latest"
RECHECK_SECONDS = 15 * 60  # re-verify alliance membership this often

GUIDES_DIR = BASE_DIR / "guides"
RATES_FILE = BASE_DIR / "rates.json"