"""CrawlerPal 2.0 Server Entry Point

Evolved from positiveblue/CrawlerPal 1.0 monolithic server into the
modular, enterprise-ready CrawlerPal 2.0 architecture with PostgreSQL/SQLite,
L402 protocol, PayPal Sandbox Orders v2 capture lifecycle, AI Agent & MCP engine.
"""

import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=False)
