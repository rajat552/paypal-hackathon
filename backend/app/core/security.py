import hashlib
import hmac
import secrets
from backend.app.core.config import settings

def hash_token(raw_token: str) -> str:
    """Compute HMAC-SHA256 hash of token using SECRET_KEY to prevent rainbow table attacks."""
    return hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        raw_token.strip().encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

def verify_token_hash(raw_token: str, stored_hash: str) -> bool:
    """Constant-time token hash verification."""
    computed = hash_token(raw_token)
    return hmac.compare_digest(computed, stored_hash)

def generate_secure_bearer_token() -> str:
    """Generate cryptographically secure 256-bit token with pm_live_ prefix."""
    random_bytes = secrets.token_urlsafe(32)
    return f"pm_live_{random_bytes}"

def generate_challenge_id() -> str:
    """Generate opaque cryptographically random challenge identifier."""
    return f"chl_{secrets.token_hex(16)}"

def hash_password(password: str) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with random salt."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000
    )
    return f"{salt}:{key.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against salt:key PBKDF2 format."""
    try:
        salt, key_hex = hashed_password.split(":", 1)
        key = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            salt.encode("utf-8"),
            100_000
        )
        return hmac.compare_digest(key.hex(), key_hex)
    except Exception:
        return False

