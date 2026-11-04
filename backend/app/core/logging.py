import logging
import re
import sys

from backend.app.core.config import settings

REDACT_PATTERNS = [
    (re.compile(r'(Bearer\s+)([A-Za-z0-9_\-\.]+)', re.IGNORECASE), r'\1[REDACTED_TOKEN]'),
    (re.compile(r'(client_secret=)([^\s&]+)', re.IGNORECASE), r'\1[REDACTED_SECRET]'),
    (re.compile(r'(password=)([^\s&]+)', re.IGNORECASE), r'\1[REDACTED_PASSWORD]'),
    (re.compile(r'(PAYPAL_CLIENT_SECRET=)([^\s&]+)', re.IGNORECASE), r'\1[REDACTED_SECRET]'),
    (re.compile(r'("access_token"\s*:\s*")([^"]+)(")', re.IGNORECASE), r'\1[REDACTED_TOKEN]\3'),
]

class RedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        original = super().format(record)
        redacted = original
        for pattern, replacement in REDACT_PATTERNS:
            redacted = pattern.sub(replacement, redacted)
        return redacted

def setup_logging():
    logger = logging.getLogger("paymesh")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    
    # Avoid duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = RedactingFormatter(
            fmt="%(asctime)s [%(levelname)s] [paymesh] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    return logger

logger = setup_logging()

