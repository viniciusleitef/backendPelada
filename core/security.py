import os
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

PASSWORD_SALT = os.getenv("PASSWORD_SALT", "pelada-salt")
TOKEN_EXPIRE_DAYS = int(os.getenv("TOKEN_EXPIRE_DAYS", "7"))

def hash_password(password: str) -> str:
    data = (PASSWORD_SALT + password).encode()
    return hashlib.sha256(data).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hmac.compare_digest(hash_password(password), hashed)

def generate_token() -> str:
    return secrets.token_urlsafe(32)

def token_expiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRE_DAYS)
from core.config import load_dotenv
load_dotenv()
