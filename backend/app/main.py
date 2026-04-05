from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.config import get_settings
from app.logging_config import configure_logging
from app.metrics import BACKEND_UP
from app.middleware import ObservabilityMiddleware, SecurityHeadersMiddleware
from app.routers.events import router as events_router
from app.routers.ops import router as ops_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    settings = get_settings()
    BACKEND_UP.set(1)
    logger.info(
        "application_started",
        extra={"extra_fields": {"environment": settings.environment}},
    )
    yield
    BACKEND_UP.set(0)
    logger.info("application_stopped")


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_host_list,
    )
    application.add_middleware(SecurityHeadersMiddleware)
    application.add_middleware(ObservabilityMiddleware)
    application.include_router(events_router)
    application.include_router(ops_router)
    return application


app = create_app()
