import pytest
from backend.app.core.config import settings
from backend.app.core.security import (
    hash_token, verify_token_hash,
    generate_secure_bearer_token, generate_challenge_id,
    hash_password, verify_password
)

def test_settings_properties():
    assert settings.APP_BASE_URL is not None
    assert settings.paypal_base_url in ("https://api-m.sandbox.paypal.com", "https://api-m.paypal.com")
    assert settings.PAYMENT_CHALLENGE_TTL_MINUTES == 10

def test_token_hashing_and_verification():
    raw_token = generate_secure_bearer_token()
    assert raw_token.startswith("pm_live_")
    
    token_hash = hash_token(raw_token)
    assert len(token_hash) == 64 # SHA-256 hex length
    assert verify_token_hash(raw_token, token_hash) is True
    assert verify_token_hash("pm_live_wrong_token", token_hash) is False

def test_challenge_id_format():
    chl_id = generate_challenge_id()
    assert chl_id.startswith("chl_")
    assert len(chl_id) >= 20

def test_password_hashing():
    pw = "SuperSecretPassword2026!"
    hashed = hash_password(pw)
    assert verify_password(pw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False
