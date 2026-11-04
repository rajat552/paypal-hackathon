from fastapi import APIRouter

from backend.app.api.v1.routes.agent import router as agent_router
from backend.app.api.v1.routes.analytics import router as analytics_router
from backend.app.api.v1.routes.catalogue import router as catalogue_router
from backend.app.api.v1.routes.payments import router as payments_router
from backend.app.api.v1.routes.publisher import router as publisher_router
from backend.app.api.v1.routes.resources import router as resources_router

api_router = APIRouter()
api_router.include_router(catalogue_router)
api_router.include_router(resources_router)
api_router.include_router(payments_router)
api_router.include_router(agent_router)
api_router.include_router(publisher_router)
api_router.include_router(analytics_router)

__all__ = ["api_router"]
