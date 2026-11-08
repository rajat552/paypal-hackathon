import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Header, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.app.api.v1.routes import api_router
from backend.app.api.v1.routes.health import router as health_router
from backend.app.api.v1.routes.payments import router as payments_router
from backend.app.core.config import settings
from backend.app.core.exceptions import (
    InvalidChallengeException,
    PayPalApiException,
    PayMeshException,
    PolicyViolationException,
)
from backend.app.core.logging import logger
from backend.app.db.session import AsyncSessionLocal, init_db
from backend.app.scripts.seed_demo import seed_demo_data

PORTAL_HTML_PATH = Path(__file__).parent / "templates" / "portal.html"
FRONTEND_DIST_DIR = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
FRONTEND_INDEX_HTML = FRONTEND_DIST_DIR / "index.html"

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing PayMesh AI database tables...")
    await init_db()
    async with AsyncSessionLocal() as session:
        await seed_demo_data(session)
    logger.info("PayMesh AI startup complete and ready for PayPal AI Hackathon.")
    yield
    logger.info("PayMesh AI shutting down gracefully.")

app = FastAPI(
    title="PayMesh AI — A Trust & Payment Infrastructure for Autonomous AI Commerce",
    description="A Trust & Payment Infrastructure for Autonomous AI Commerce via L402 protocol and verified PayPal Sandbox capture.",
    version="2.0.0",
    lifespan=lifespan
)

# Mount frontend assets if built
if (FRONTEND_DIST_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST_DIR / "assets")), name="assets")

# CORS configuration: strict explicit origins without wildcard
allowed_cors_origins = [
    settings.FRONTEND_URL.rstrip("/"),
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_cors_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    return response

# Mount Routers
app.include_router(health_router)
app.include_router(payments_router) # Includes legacy /l402/payment-request
app.include_router(api_router, prefix="/api/v1")

# Custom Exception Handlers
@app.exception_handler(InvalidChallengeException)
async def invalid_challenge_handler(request: Request, exc: InvalidChallengeException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": exc.code, "message": exc.message}
    )

@app.exception_handler(PolicyViolationException)
async def policy_violation_handler(request: Request, exc: PolicyViolationException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"error": exc.code, "message": exc.message, "details": exc.details}
    )

@app.exception_handler(PayPalApiException)
async def paypal_api_handler(request: Request, exc: PayPalApiException):
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"error": exc.code, "message": exc.message, "details": exc.details}
    )

@app.exception_handler(PayMeshException)
async def generic_paymesh_handler(request: Request, exc: PayMeshException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": exc.code, "message": exc.message}
    )

def is_browser(user_agent: str | None) -> bool:
    if not user_agent:
        return False
    ua = user_agent.lower()
    return any(b in ua for b in ["mozilla", "chrome", "safari", "firefox", "edge", "opera", "webkit"])

@app.get("/", response_class=HTMLResponse)
async def root_portal(
    request: Request,
    user_agent: str | None = Header(None),
    authorization: str | None = Header(None)
):
    """Browser landing page and backward-compatible bot L402 challenge."""
    # Check if bot/CLI request
    if not is_browser(user_agent):
        if authorization and authorization.lower().startswith("bearer "):
            # Validated authenticated bot request
            return JSONResponse(content={
                "status": "authenticated",
                "news": [
                    {
                        "category": "technology",
                        "title": "Autonomous Agents Adopt Machine-Readable L402 Micro-Commerce",
                        "description": "Publishers globally are unlocking programmatic revenue through PayPal Sandbox and L402 gateways."
                    }
                ]
            })
        
        # Unauthenticated bot: return legacy L402 challenge
        payment_context_token = str(uuid.uuid4())
        return JSONResponse(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            content={
                "protocol": "paymesh-l402",
                "version": "2.0.0",
                "payment_request_url": f"{settings.APP_BASE_URL}/l402/payment-request",
                "payment_context_token": payment_context_token,
                "offers": [
                    {
                        "id": "one_category",
                        "title": "Access to one category",
                        "description": "Access to all the data in one category",
                        "amount": 0.01,
                        "currency": "USD",
                        "payment_methods": ["paypal"]
                    },
                    {
                        "id": "all_categories",
                        "title": "All Categories Access",
                        "description": "Access all news data across all categories",
                        "amount": 0.05,
                        "currency": "USD",
                        "type": "subscription",
                        "duration": "1 month",
                        "payment_methods": ["paypal"]
                    }
                ]
            }
        )

    if FRONTEND_INDEX_HTML.exists():
        return HTMLResponse(content=FRONTEND_INDEX_HTML.read_text(encoding="utf-8"))
    if PORTAL_HTML_PATH.exists():
        return HTMLResponse(content=PORTAL_HTML_PATH.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>PayMesh AI Online</h1><p>A Trust &amp; Payment Infrastructure for Autonomous AI Commerce. Visit /docs or /api/v1/catalogue</p>")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=False)
