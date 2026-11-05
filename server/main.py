"""PayMesh AI Server Entry Point

Enterprise-ready PayMesh AI architecture with PostgreSQL/SQLite,
L402 protocol, PayPal Sandbox Orders v2 capture lifecycle, AI Agent & MCP engine.
"""

import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.main import app  # noqa: E402

__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=False)
